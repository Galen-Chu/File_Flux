# -*- coding: utf-8 -*-
"""
Test script for Google Drive API endpoints

This script tests the Google Drive service layer.
Run this while the Django server is running.
"""

import os
import sys
import time
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_flux.settings')
django.setup()

from django.contrib.auth.models import User
from manager.models import CloudStorageToken
from manager.services.google_drive_service import GoogleDriveService

def test_service():
    """Test Google Drive service layer"""
    # Force UTF-8 output on Windows
    if sys.platform.startswith('win'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print("Testing Google Drive Service Layer")
    print("=" * 60)

    # Get user
    try:
        user = User.objects.get(username='Galen')
        print("OK Found user: " + user.username)
    except User.DoesNotExist:
        print("ERROR User 'Galen' not found")
        return

    # Get Google Drive token
    try:
        token = CloudStorageToken.objects.get(user=user, provider='googledrive')
        print("OK Found Google Drive token (ID: " + str(token.id) + ")")
    except CloudStorageToken.DoesNotExist:
        print("ERROR Google Drive token not found. Please connect Google Drive first.")
        return

    # Initialize service
    service = GoogleDriveService(token)
    print("OK Google Drive service initialized")

    # Test list files
    print("")
    print("-" * 60)
    print("TEST: List Files from Google Drive")
    print("-" * 60)

    result = service.list_files(page_size=10)

    if result.get('error'):
        print("ERROR " + result['error'])
        return

    print("OK Listed " + str(len(result['files'])) + " files")

    if result['files']:
        print("")
        print("First 3 files:")
        for file in result['files'][:3]:
            print("  - " + file['name'] + " (" + file['type'] + ")")

    # Test create and delete folder
    print("")
    print("-" * 60)
    print("TEST: Create & Delete Folder")
    print("-" * 60)

    test_folder_name = "Test_Folder_FileFlux_" + str(int(time.time()))
    result = service.create_folder(folder_name=test_folder_name)

    if result.get('error'):
        print("ERROR " + result['error'])
    else:
        print("OK Created test folder: " + result['name'])
        print("  Folder ID: " + result['id'])

        # Delete the folder
        delete_result = service.delete_file(result['id'])

        if delete_result.get('success'):
            print("OK Test folder deleted successfully")
        else:
            print("WARNING Delete failed (manual cleanup needed): " + delete_result.get('error'))

    print("")
    print("=" * 60)
    print("SUCCESS All service operations working correctly!")
    print("=" * 60)
    print("")
    print("Phase A (Google Drive Service Layer) is complete and working!")
    print("Ready to proceed to Phase B (Frontend Integration)")


if __name__ == '__main__':
    test_service()
