from django.urls import path, include
from rest_framework import routers, renderers
from . import api


urlpatterns = [
    path('', api.LessonViewSet.as_view({"get": "list", "post": "create"})),
    path('<int:pk>/', api.LessonViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"})),
    path('<int:pk>/students/', api.LessonViewSet.as_view({"get": "list_students"})),
    path('<int:lpk>/students/<int:spk>/', api.LessonViewSet.as_view({"post": "add_student", "delete": "remove_student"})),

    
]