"""
Cloud drive OAuth views
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.cloud_manager import CloudDriveManager
from .models import CloudStorageToken


@login_required
def connect_onedrive(request):
    """
    Initiate OneDrive OAuth connection
    """
    try:
        auth_url = CloudDriveManager.get_authorization_url('onedrive')

        # For demo purposes, simulate successful connection
        # In production, this would redirect to actual OAuth URL
        messages.info(request, 'OneDrive integration requires Microsoft Azure app registration. See documentation for setup instructions.')

        # Simulate connection for demo
        if request.GET.get('demo') == 'true':
            success = CloudDriveManager.connect_drive(
                user=request.user,
                provider='onedrive',
                access_token='demo_access_token',
                refresh_token='demo_refresh_token',
                expires_in=3600
            )
            if success:
                messages.success(request, 'OneDrive connected successfully (demo mode)!')
                return redirect('manager:profile')

        return redirect('manager:profile')

    except Exception as e:
        messages.error(request, f'Failed to connect OneDrive: {str(e)}')
        return redirect('manager:profile')


@login_required
def connect_googledrive(request):
    """
    Initiate Google Drive OAuth connection
    """
    try:
        auth_url = CloudDriveManager.get_authorization_url('googledrive')

        # For demo purposes, simulate successful connection
        # In production, this would redirect to actual OAuth URL
        messages.info(request, 'Google Drive integration requires Google Cloud project setup. See documentation for setup instructions.')

        # Simulate connection for demo
        if request.GET.get('demo') == 'true':
            success = CloudDriveManager.connect_drive(
                user=request.user,
                provider='googledrive',
                access_token='demo_access_token',
                refresh_token='demo_refresh_token',
                expires_in=3600
            )
            if success:
                messages.success(request, 'Google Drive connected successfully (demo mode)!')
                return redirect('manager:profile')

        return redirect('manager:profile')

    except Exception as e:
        messages.error(request, f'Failed to connect Google Drive: {str(e)}')
        return redirect('manager:profile')


@login_required
@require_POST
def disconnect_drive(request, provider):
    """
    Disconnect a cloud drive
    """
    try:
        success = CloudDriveManager.disconnect_drive(request.user, provider)

        if success:
            messages.success(request, f'{provider.title()} disconnected successfully!')
        else:
            messages.warning(request, f'{provider.title()} was not connected.')

    except Exception as e:
        messages.error(request, f'Failed to disconnect {provider}: {str(e)}')

    return redirect('manager:profile')


@login_required
def cloud_status(request):
    """
    Get cloud drive connection status (API endpoint)
    """
    drives = CloudDriveManager.get_connected_drives(request.user)

    return JsonResponse({
        'drives': drives,
        'total': len(drives)
    })
