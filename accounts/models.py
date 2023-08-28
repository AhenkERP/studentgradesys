from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=80, blank=True,verbose_name="Name",null=True)
    surname = models.CharField(max_length=60, blank=True,verbose_name="Surname",null=True)
    dateofbirth = models.DateField(blank=True,verbose_name="Date of Birth",null=True)
    phone = models.CharField(max_length=32, blank=True,verbose_name="Phone Number",null=True)
    mobile = models.CharField(max_length=32, blank=True,verbose_name="Mobile Number",null=True)
    country = models.CharField(max_length=50, verbose_name="Country",default="Türkiye",null=True)
    state = models.CharField(max_length=60, blank=True,verbose_name="State / Province",null=True)
    city = models.CharField(max_length=90, blank=True,verbose_name="City",null=True)
    address= models.CharField(max_length=100, blank=True,verbose_name="Address",null=True)
    zip_code= models.CharField(max_length=6, blank=True,verbose_name="Zip Code",null=True)
    identity_number = models.CharField(max_length=13, blank=True,verbose_name="Identity Number",null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_created_by", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_updated_by", null=True)

    def __str__(self):
        return "%s %s" % (self.name, self.surname)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, admin_user=None, **kwargs):
    '''
    Updates profile of the user when user is created or updated.
    '''
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()





