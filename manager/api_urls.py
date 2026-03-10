"""
API URL configuration for file management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import FileManagementViewSet
from .cloud_api_views import CloudDriveViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'files', FileManagementViewSet, basename='files')
router.register(r'cloud', CloudDriveViewSet, basename='cloud')

urlpatterns = [
    path('', include(router.urls)),
]
