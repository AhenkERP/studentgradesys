from django.urls import path, include
from rest_framework import routers, renderers
from . import api
from accounts import api as accounts_api

urlpatterns = [
    path('', api.UserViewSet.as_view({"get": "list", "post": "create"})),
    path('<int:pk>/', api.UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"})),
    path('profile/', accounts_api.StudentViewSet.as_view({"get": "list", "post": "create"})),
    path('profile/<int:pk>/', accounts_api.StudentViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"})),
]