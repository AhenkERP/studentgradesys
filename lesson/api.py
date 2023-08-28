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
from .models import Lesson

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class LessonSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_teacher(self, obj):
        if not obj.teacher:
            return None
        return {
            'id': obj.teacher.id,
            'full_name': self.user_full_name(obj.teacher),
            'email': obj.teacher.email,
            'dateofbirth': obj.teacher.profile.dateofbirth,
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
    
    def get_students(self, obj):
        students = []
        for student in obj.students.all():
            students.append({
                'id': student.id,
                'full_name': self.user_full_name(student),
                'email': student.email,
                'dateofbirth': student.profile.dateofbirth,
            })
        return students
    
    def user_full_name(self, obj):
        name = obj.profile.name if obj.profile.name else ''
        surname = obj.profile.surname if obj.profile.surname else ''
        return name + ' ' + surname
    


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = {
            'name': SearchConstants.STRING,
            'description': SearchConstants.STRING,
            'period': SearchConstants.STRING,
        }


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filterset_class = LessonFilter
    # permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    authentication_classes = [OAuth2Authentication]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'list_students' or self.action == 'retrieve':
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
        Get list of all lessons.
        '''
        try:
            queryset = Lesson.objects.all().select_related('created_by', 'updated_by', 'teacher', 'students').order_by('id')
            return super().list(queryset, *args, **kwargs)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None, *args, **kwargs):
        '''
        Get details of a lesson.
        '''
        try:
            queryset = Lesson.objects.all()
            lesson = get_object_or_404(queryset, pk=pk)
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def create(self, request, *args, **kwargs):
        '''
        Create a lesson.
        '''
        try:
            serializer = LessonSerializer(data=request.data)
            if serializer.is_valid():
                # add created_by field to serializer data
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk=None, *args, **kwargs):
        '''
        Update a lesson.
        '''
        try:
            queryset = Lesson.objects.all()
            lesson = get_object_or_404(queryset, pk=pk)
            serializer = LessonSerializer(lesson, data=request.data)
            if serializer.is_valid():
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None, *args, **kwargs):
        '''
        Delete a lesson.
        '''
        try:
            queryset = Lesson.objects.all()
            lesson = get_object_or_404(queryset, pk=pk)
            lesson.delete()
            return self.success('Lesson deleted.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    def partial_update(self, request, pk=None, *args, **kwargs):
        '''
        Partial update a lesson.
        '''
        try:
            queryset = Lesson.objects.all()
            lesson = get_object_or_404(queryset, pk=pk)
            serializer = LessonSerializer(lesson, data=request.data, partial=True)
            if serializer.is_valid():
                if request.data.get('teacher'):
                    teacher = User.objects.filter(pk=request.data.get('teacher')).first()
                    if not teacher:
                        return self.fail('Teacher not found.')
                    serializer.validated_data['teacher'] = teacher
                # add updated_by field to serializer data
                serializer.validated_data['updated_by'] = request.user
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # add student to lesson
    def add_student(self, request, lpk=None, spk=None, *args, **kwargs):
        '''
        Add student to lesson.
        @lpk: lesson id
        @spk: student id
        '''
        try:
            lesson = Lesson.objects.filter(pk=lpk).first()
            if not lesson:
                return self.fail('Lesson not found.')
            student = User.objects.filter(pk=spk).first()
            if not student:
                return self.fail('Student not found.')

            if student in lesson.students.all():
                return self.fail('Student already in lesson.')
            lesson.students.add(student)
            lesson.save()
            return self.success('Student added to lesson.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # remove student from lesson
    def remove_student(self, request, lpk=None, spk=None, *args, **kwargs):
        '''
        Remove student from lesson.
        @lpk: lesson id
        @spk: student id
        '''
        try:
            lesson = Lesson.objects.filter(pk=lpk).first()
            if not lesson:
                return self.fail('Lesson not found.')
            student = User.objects.filter(pk=spk).first()
            if not student:
                return self.fail('Student not found.')
            if student not in lesson.students.all():
                return self.fail('Student not in lesson.')
            lesson.students.remove(student)
            lesson.save()
            return self.success('Student removed from lesson.')
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def user_full_name(self, obj):
        name = obj.profile.name if obj.profile.name else ''
        surname = obj.profile.surname if obj.profile.surname else ''
        return name + ' ' + surname

    # list students of lesson
    def list_students(self, request, pk=None, *args, **kwargs):
        '''
        List students of lesson.
        @pk: lesson id
        '''
        try:
            lesson = Lesson.objects.filter(pk=pk).first()
            if not lesson:
                return self.fail('Lesson not found.')
            students = []
            for student in lesson.students.all():
                students.append({
                    'id': student.id,
                    'full_name': self.user_full_name(student),
                    'email': student.email,
                    'dateofbirth': student.profile.dateofbirth,
                })
            return Response(students)
        except Exception as e:
            logging.getLogger('db').exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)