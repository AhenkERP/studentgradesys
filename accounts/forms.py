from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.utils import timezone


class ProfileUpdateForm(forms.ModelForm):
    '''
    Form for updating profile of the user.
    '''
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'updated_by']
        widgets = {
            'user': forms.HiddenInput(),
        }

    def save(self, commit=True, admin_user=None):
        '''
        Saves the form and updates the profile of the user. 
        
        We get admin_user parameter to note user who updated the profile.
        '''
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            profile, _ = Profile.objects.get_or_create(user=instance.user)
            profile.updated_at = timezone.now()
            
            if admin_user:
                # If admin_user is given, it means that profile is updated by admin.
                profile.updated_by = admin_user
            else:
                # If admin_user is not given, it means that profile is updated by user.
                profile.updated_by = instance
            
            profile.save()
            
        return instance


