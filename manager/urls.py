from django.urls import path
from .views import IndexView, FileManagerView
from .auth_views import register_view, login_view, logout_view, profile_view
from .cloud_views import (
    connect_onedrive,
    connect_googledrive,
    disconnect_drive,
    cloud_status
)
from .oauth_views import oauth_callback

app_name = 'manager'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('manager/', FileManagerView.as_view(), name='file_manager'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('cloud/connect/onedrive/', connect_onedrive, name='connect_onedrive'),
    path('cloud/connect/googledrive/', connect_googledrive, name='connect_googledrive'),
    path('cloud/disconnect/<str:provider>/', disconnect_drive, name='disconnect_drive'),
    path('cloud/status/', cloud_status, name='cloud_status'),
    # OAuth callback (unified for all providers)
    path('oauth/callback/', oauth_callback, name='oauth_callback'),
]
