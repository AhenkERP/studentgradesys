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
from lesson.models import Lesson
from .models import Grade
from accounts.models import Profile
from lesson.api import LessonSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = '__all__'

    def get_student(self, obj):
        if not obj.student:
            return None
        return {
            'id': obj.student.id,
            'full_name': self.user_full_name(obj.student),
            'email': obj.student.email,
            'dateofbirth': obj.student.profile.dateofbirth,
        }
    
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
    
    def get_lesson(self, obj):
        if not obj.lesson:
            return None
        return LessonSerializer(obj.lesson).data
         
    
    def user_full_name(self, obj):
        name = obj.profile.name if obj.profile.name else ''
        surname = obj.profile.surname if obj.profile.surname else ''
        return name + ' ' + surname
    


class GradeFilter(filters.FilterSet):
    class Meta:
        model = Grade
        fields = {
            'lesson__name': SearchConstants.STRING,
            'description': SearchConstants.STRING,
            'date': SearchConstants.DATE,
        }


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filterset_class = GradeFilter
    authentication_classes = [OAuth2Authentication]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'list_student_grades':
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
    

    def list(self, request, *args, **kwargs):
        '''
        Get list of all grades.
        '''
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        '''
        Get details of a grade.
        '''
        try:
            queryset = Grade.objects.all()
            grade = get_object_or_404(queryset, pk=pk)
            serializer = GradeSerializer(grade)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    def create(self, request):
        '''
        Create a new grade.
        '''
        try:
            if request.data.get('student'):
                student = Profile.objects.filter(pk=request.data.get('student')).first()
                if not student:
                    return self.fail('Student not found')
            if request.data.get('lesson'):
                lesson = Lesson.objects.filter(pk=request.data.get('lesson')).first()
                if not lesson:
                    return self.fail('Lesson not found')
            serializer = GradeSerializer(data=request.data)
            if request.data.get('student'):
                serializer.student = student.user
            if request.data.get('lesson'):
                serializer.lesson = lesson
            if serializer.is_valid():
                serializer.save(created_by=request.user, updated_by=request.user)
                return Response(serializer.data)
                return self.success('Grade created successfully')
            return self.fail(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self, request, pk=None):
        '''
        Update a grade.
        '''
        try:
            queryset = Grade.objects.all()
            grade = get_object_or_404(queryset, pk=pk)
            serializer = GradeSerializer(grade, data=request.data)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                return Response(serializer.data)
                return self.success('Grade updated successfully')
            return self.fail(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, pk=None):
        '''
        Delete a grade.
        '''
        try:
            queryset = Grade.objects.all()
            grade = get_object_or_404(queryset, pk=pk)
            grade.delete()
            return self.success('Grade deleted successfully')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def partial_update(self, request, pk=None):
        '''
        Partial update a grade.
        '''
        try:
            queryset = Grade.objects.all()
            grade = get_object_or_404(queryset, pk=pk)
            if not grade:
                return self.fail('Grade not found')
            if request.data.get('student'):
                student = Profile.objects.filter(pk=request.data.get('student')).first()
                if not student:
                    return self.fail('Student not found')
            if request.data.get('lesson'):
                lesson = Lesson.objects.filter(pk=request.data.get('lesson')).first()
                if not lesson:
                    return self.fail('Lesson not found')
            serializer = GradeSerializer(grade, data=request.data, partial=True)
            
            if serializer.is_valid():
                if request.data.get('student'):
                    serializer.validated_data['student'] = Profile.objects.filter(pk=request.data.get('student')).first().user
                if request.data.get('lesson'):
                    serializer.validated_data['lesson'] = Lesson.objects.filter(pk=request.data.get('lesson')).first()
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
                # return self.success('Grade updated successfully')
            return self.fail(serializer.errors)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # get all grades of a student
    def list_student_grades(self, request, pk=None):
        '''
        Get list of all grades of a student.
        '''
        try:
            if not pk:
                return self.fail('Student id is required')
            if not Profile.objects.filter(pk=pk).exists():
                return self.fail('Student not found')
            if not request.user.is_staff and request.user.id != pk:
                return self.fail('You are not allowed to view this student grades')
            student = Profile.objects.filter(pk=pk).first()
            queryset = Grade.objects.filter(student__pk=student.user.pk)
            serializer = GradeSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
    # get all grades of a lesson
    def list_lesson_grades(self, request, pk=None):
        '''
        Get list of all grades of a lesson.
        '''
        try:
            if not pk:
                return self.fail('Lesson id is required')
            if not Lesson.objects.filter(pk=pk).exists():
                return self.fail('Lesson not found')
            queryset = Grade.objects.filter(lesson=pk)
            serializer = GradeSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    # get all grades of a teacher
    def list_teacher_grades(self, request, pk=None):
        '''
        Get list of all grades of a teacher.
        '''
        try:
            if not pk:
                return self.fail('Teacher id is required')
            if not User.objects.filter(pk=pk).exists():
                return self.fail('Teacher not found')
            queryset = Grade.objects.filter(lesson__teacher__pk=pk)
            serializer = GradeSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)