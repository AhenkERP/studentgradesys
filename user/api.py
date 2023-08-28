from rest_framework import serializers, viewsets, permissions, generics, renderers
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from custom.constants import SearchConstants
from django.shortcuts import get_object_or_404
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import permissions
import logging
from accounts.models import Profile

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        except_fields = ['password']


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': SearchConstants.STRING,
            'email': SearchConstants.STRING,
            'first_name': SearchConstants.STRING,
            'last_name': SearchConstants.STRING,
        }

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    authentication_classes = [OAuth2Authentication]

    # return success with message
    def success(self, message):
        return Response({'success': True, 'message': message}, status=status.HTTP_200_OK)
    
    # return success = False with message
    def fail(self, message):
        return Response({'success': False, 'message': message}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        '''
        Get list of all users.
        '''
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None, *args, **kwargs):
        '''
        Get details of a user.
        '''
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def create(self, request):
        '''
        Create a new user.
        '''
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # save user
                user_instance = serializer.save()
                # get password from serializer data
                password = serializer.data.get('password')
                # set user password
                user_instance.set_password(password)
                user_instance.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                # get password from serializer data
                password = serializer.data.get('password')
                # set user password
                user_instance.set_password(password)
                user_instance.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            user.delete()
            return self.success('User deleted successfully.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def partial_update(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                user_instance = serializer.save()
                if 'password' in serializer.data:
                    # get password from serializer data
                    password = serializer.data.get('password')
                    # set user password
                    user_instance.set_password(password)
                    user_instance.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

