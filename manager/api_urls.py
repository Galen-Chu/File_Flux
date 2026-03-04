"""
API URL configuration for file management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import FileManagementViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r'files', FileManagementViewSet, basename='files')

urlpatterns = [
    path('', include(router.urls)),
]
