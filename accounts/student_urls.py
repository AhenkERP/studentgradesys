from django.urls import path
from . import api

urlpatterns = [
    path('', api.StudentViewSet.as_view({"get": "list"})),
    path('self/', api.StudentViewSet.as_view({"get": "get_own_profile"})),
    path('<int:pk>/', api.StudentViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update"})),
    path('user/<int:pk>/', api.StudentViewSet.as_view({"get": "retrieve_by_user_id", "put": "update_by_user_id", "destroy": "destroy_by_user_id", "patch": "partial_update_by_user_id"})),
    path('<int:spk>/lessons/', api.StudentViewSet.as_view({"get": "list_lessons"})),
    path('<int:spk>/lessons/<int:lpk>/', api.StudentViewSet.as_view({"post": "add_lesson", "delete": "remove_lesson"})),
]