from django.urls import path, include
from . import api


urlpatterns = [
    path('', api.GradeViewSet.as_view({"get": "list", "post": "create"})),
    path('<int:pk>/', api.GradeViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"})),
    path('list/student/<int:pk>/', api.GradeViewSet.as_view({"get": "list_student_grades"})),
    path('list/lesson/<int:pk>/', api.GradeViewSet.as_view({"get": "list_lesson_grades"})),
    path('list/teacher/<int:pk>/', api.GradeViewSet.as_view({"get": "list_teacher_grades"})),
]