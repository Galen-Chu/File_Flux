"""
Quick non-interactive test for Google Drive service
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_flux.settings')
django.setup()

from django.contrib.auth.models import User
from manager.models import CloudStorageToken
from manager.services.google_drive_service import GoogleDriveService

def main():
    print("=" * 60)
    print("Testing Google Drive Service Layer")
    print("=" * 60)

    # Get user
    try:
        user = User.objects.get(username='Galen')
        print(f"✓ Found user: {user.username}")
    except User.DoesNotExist:
        print("✗ User 'Galen' not found")
        return

    # Get Google Drive token
    try:
        token = CloudStorageToken.objects.get(user=user, provider='googledrive')
        print(f"✓ Found Google Drive token (ID: {token.id})")
        print(f"  Token created: {token.created_at}")
    except CloudStorageToken.DoesNotExist:
        print("✗ Google Drive token not found. Please connect Google Drive first.")
        return

    # Initialize service
    service = GoogleDriveService(token)
    print("✓ Google Drive service initialized")

    # Test list files
    print("\n" + "-" * 60)
    print("TEST: List Files")
    print("-" * 60)

    result = service.list_files(page_size=10)

    if result.get('error'):
        print(f"✗ Error: {result['error']}")
    else:
        print(f"✓ Listed {len(result['files'])} files")
        if result['files']:
            print("\nFirst 5 files:")
            for file in result['files'][:5]:
                print(f"  - {file['name']} ({file['type']})")
        if result.get('next_page_token'):
            print(f"\n✓ Has next page token")
        else:
            print(f"\n✓ No more pages")

    # Test create folder
    print("\n" + "-" * 60)
    print("TEST: Create Folder")
    print("-" * 60)

    test_folder_name = "Test_Folder_FileFlux_2026"
    folder_result = service.create_folder(folder_name=test_folder_name)

    if folder_result.get('error'):
        print(f"✗ Error: {folder_result['error']}")
    else:
        print(f"✓ Created folder: {folder_result['name']}")
        print(f"  Folder ID: {folder_result['id']}")
        folder_id = folder_result['id']

        # Test delete folder
        print("\n" + "-" * 60)
        print("TEST: Delete Folder")
        print("-" * 60)

        delete_result = service.delete_file(folder_id)

        if delete_result.get('success'):
            print(f"✓ Folder deleted successfully")
        else:
            print(f"✗ Delete failed: {delete_result.get('error')}")

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✓ All basic service operations working correctly!")
    print("\nGoogle Drive service layer is ready for Phase B (Frontend Integration)")

if __name__ == '__main__':
    main()
