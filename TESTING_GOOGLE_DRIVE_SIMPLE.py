# -*- coding: utf-8 -*-
"""
Simple Google Drive service test
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_flux.settings')
django.setup()

from django.contrib.auth.models import User
from manager.models import CloudStorageToken
from manager.services.google_drive_service import GoogleDriveService

def main():
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
        print("ERROR Google Drive token not found")
        return

    # Initialize service
    service = GoogleDriveService(token)
    print("OK Google Drive service initialized")

    # Test list files
    print("")
    print("-" * 60)
    print("TEST: List Files")
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

    print("")
    print("=" * 60)
    print("SUCCESS Google Drive service is working!")
    print("=" * 60)

if __name__ == '__main__':
    main()
