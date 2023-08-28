"""
URL configuration for StudentGradeSystem project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include ('home.urls')),
    path('api/users/', include ('user.urls')),
    path('api/students/', include ('accounts.student_urls')),
    path('api/lessons/', include ('lesson.urls')),
    path('api/grades/', include ('grade.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

handler403 = 'home.views.error403'
handler404 = 'home.views.error404'
handler500 = 'home.views.error500'
admin.site.site_header = 'SGS Admin'
admin.site.site_title = 'SGS Admin'