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
from .models import Profile
from lesson.models import Lesson
from lesson.api import LessonSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class StudentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = '__all__'

    def get_created_by(self, obj):
        if not obj.created_by:
            return None
        return {
            'id': obj.created_by.id,
            'full_name':self.user_full_name(obj.created_by),
            'email': obj.created_by.email,
            'dateofbirth': obj.created_by.profile.dateofbirth,
        }
    
    def get_updated_by(self, obj):
        if not obj.updated_by:
            return None
        return {
            'id': obj.updated_by.id,
            'full_name': self.user_full_name(obj.updated_by),
            'email': obj.updated_by.email,
            'dateofbirth': obj.updated_by.profile.dateofbirth,
        }

    def user_full_name(self, obj):
        name = obj.profile.name if obj.profile.name else ''
        surname = obj.profile.surname if obj.profile.surname else ''
        return name + ' ' + surname

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Profile
        fields = {
            'name': SearchConstants.STRING,
            'surname': SearchConstants.STRING,
            'dateofbirth': SearchConstants.DATE,
            'identity_number': SearchConstants.STRING,
        }

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    authentication_classes = [OAuth2Authentication]

    def get_permissions(self):
        if self.action == 'list_lessons' or self.action == 'retrieve' or self.action == 'get_own_profile':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    # return success with message
    def success(self, message):
        return Response({'success': True, 'message': message}, status=status.HTTP_200_OK)
    
    # return success = False with message
    def fail(self, message):
        return Response({'success': False, 'message': message}, status=status.HTTP_200_OK)

    # Get all Students (Profiles)
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Get a Student (Profile) by User ID
    def retrieve_by_user_id(self, request, pk=None, *args, **kwargs):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, user=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Get a Student (Profile) by ID
    def retrieve(self, request, pk=None):
        try:
            if not request.user.is_staff and request.user.id != pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # get own profile
    def get_own_profile(self, request, *args, **kwargs):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    # Create a new Student (Profile)
    # Profile is created automatically when a new user is created.
        

    # Update a Student (Profile)
    def update(self, request, pk=None):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, pk=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # Update a Student (Profile) by User ID
    def update_by_user_id(self, request, pk=None):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, user=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Delete a Student (Profile)
    # Profile is deleted automatically when a user is deleted.

    # Delete a Student (Profile) by User ID
    def destroy_by_user_id(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Partial update a Student (Profile)
    def partial_update(self, request, pk=None):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, pk=pk)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Partial update a Student (Profile) by User ID
    def partial_update_by_user_id(self, request, pk=None):
        try:
            queryset = Profile.objects.all()
            student = get_object_or_404(queryset, user=pk)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # add lesson to student
    def add_lesson(self, request, spk=None, lpk=None, *args, **kwargs):
        '''
        Add lesson to student.
        @spk: student id
        @lpk: lesson id
        '''
        try:
            student = Profile.objects.filter(pk=spk).first()
            if not student:
                return self.fail('Student not found.')
            lesson = Lesson.objects.filter(pk=lpk).first()
            if not lesson:
                return self.fail('Lesson not found.')
            if student.user in lesson.students.all():
                return self.fail('Student already added to lesson.')
            lesson.students.add(student.user)
            lesson.save()
            return self.success('Lesson added to student.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # remove lesson from student
    def remove_lesson(self, request, spk=None, lpk=None, *args, **kwargs):
        '''
        Remove lesson from student.
        @spk: student id
        @lpk: lesson id
        '''
        try:
            student = Profile.objects.filter(pk=spk).first()
            if not student:
                return self.fail('Student not found.')
            lesson = Lesson.objects.filter(pk=lpk).first()
            if not lesson:
                return self.fail('Lesson not found.')
            if not student.user in lesson.students.all():
                return self.fail('Student is not added to lesson.')
            lesson.students.remove(student.user)
            lesson.save()
            return self.success('Lesson removed from student.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # Get all lessons of student
    def list_lessons(self, request, spk=None, *args, **kwargs):
        '''
        Get all lessons of student.
        @spk: student id
        '''
        try:
            student = Profile.objects.filter(pk=spk).first()
            if not student:
                return self.fail('Student not found.')
            lessons = Lesson.objects.filter(students__in=[student.user])
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)