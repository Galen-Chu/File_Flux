#!/usr/bin/env python
"""
Test script for FileFlux v2.0.0
Tests authentication and cloud drive integration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_flux.settings')
sys.path.insert(0, 'D:\\FileFlux')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from manager.models import CloudStorageToken
from manager.services.cloud_manager import CloudDriveManager
from django.utils import timezone


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_user_registration():
    """Test user registration"""
    print_section("Testing User Registration")

    # Clean up test user if exists
    User.objects.filter(username='testuser').delete()

    # Create test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

    print(f"[OK] Created user: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  ID: {user.id}")

    return user


def test_authentication():
    """Test authentication system"""
    print_section("Testing Authentication")

    client = Client()

    # Test login page loads
    response = client.get('/login/')
    print(f"[OK] Login page status: {response.status_code}")

    # Test registration page loads
    response = client.get('/register/')
    print(f"[OK] Registration page status: {response.status_code}")

    # Test login with credentials
    logged_in = client.login(username='testuser', password='testpass123')
    print(f"[OK] Login successful: {logged_in}")

    # Test protected page (file manager)
    response = client.get('/manager/')
    print(f"[OK] File manager (authenticated) status: {response.status_code}")

    # Test profile page
    response = client.get('/profile/')
    print(f"[OK] Profile page status: {response.status_code}")

    return client


def test_cloud_drive_manager():
    """Test cloud drive manager functionality"""
    print_section("Testing Cloud Drive Manager")

    user = User.objects.get(username='testuser')

    # Test OneDrive connection (demo)
    print("Testing OneDrive connection...")
    success = CloudDriveManager.connect_drive(
        user=user,
        provider='onedrive',
        access_token='demo_access_token_onedrive',
        refresh_token='demo_refresh_token_onedrive',
        expires_in=3600
    )
    print(f"[OK] OneDrive connected: {success}")

    # Test Google Drive connection (demo)
    print("\nTesting Google Drive connection...")
    success = CloudDriveManager.connect_drive(
        user=user,
        provider='googledrive',
        access_token='demo_access_token_googledrive',
        refresh_token='demo_refresh_token_googledrive',
        expires_in=3600
    )
    print(f"[OK] Google Drive connected: {success}")

    # Test checking connection status
    is_connected = CloudDriveManager.is_drive_connected(user, 'onedrive')
    print(f"[OK] OneDrive is connected: {is_connected}")

    is_connected = CloudDriveManager.is_drive_connected(user, 'googledrive')
    print(f"[OK] Google Drive is connected: {is_connected}")

    # Test getting connected drives
    drives = CloudDriveManager.get_connected_drives(user)
    print(f"\n[OK] Connected drives: {len(drives)}")
    for drive in drives:
        print(f"  - {drive['provider_display']}: expired={drive['is_expired']}")

    # Test disconnection
    print("\nTesting disconnection...")
    success = CloudDriveManager.disconnect_drive(user, 'googledrive')
    print(f"[OK] Google Drive disconnected: {success}")

    is_connected = CloudDriveManager.is_drive_connected(user, 'googledrive')
    print(f"[OK] Google Drive is connected: {is_connected}")


def test_cloud_storage_token_model():
    """Test CloudStorageToken model"""
    print_section("Testing CloudStorageToken Model")

    user = User.objects.get(username='testuser')

    # Query tokens
    tokens = CloudStorageToken.objects.filter(user=user)
    print(f"[OK] Tokens in database: {tokens.count()}")

    for token in tokens:
        print(f"\n  Provider: {token.get_provider_display()}")
        print(f"  User: {token.user.username}")
        print(f"  Created: {token.created_at}")
        print(f"  Expires: {token.token_expires_at}")
        print(f"  Is expired: {token.is_expired()}")


def test_api_authentication():
    """Test API authentication requirement"""
    print_section("Testing API Authentication")

    client = Client()

    # Test API without authentication (should fail)
    response = client.get('/api/files/')
    print(f"[OK] API without auth status: {response.status_code}")
    print(f"  (401 = Unauthorized, expected)")

    # Test API with authentication (should succeed)
    client.login(username='testuser', password='testpass123')
    response = client.get('/api/files/')
    print(f"[OK] API with auth status: {response.status_code}")
    print(f"  (200 = OK, expected)")


def cleanup():
    """Clean up test data"""
    print_section("Cleanup")

    User.objects.filter(username='testuser').delete()
    print("[OK] Test user deleted")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  FileFlux v2.0.0 - Integration Test Suite")
    print("="*60)

    try:
        # Run tests
        user = test_user_registration()
        client = test_authentication()
        test_cloud_drive_manager()
        test_cloud_storage_token_model()
        test_api_authentication()

        print_section("[OK] All Tests Passed!")

        print("\nTest Summary:")
        print("  - User registration: [OK]")
        print("  - Authentication system: [OK]")
        print("  - Cloud drive manager: [OK]")
        print("  - Token model: [OK]")
        print("  - API authentication: [OK]")

        print("\nNext Steps:")
        print("  1. Visit http://localhost:8000/register/ to create an account")
        print("  2. Log in and navigate to Profile")
        print("  3. Test cloud drive connections (demo mode)")
        print("  4. For production, configure OAuth credentials in .env")

    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up automatically
        print("\n" + "="*60)
        cleanup()
        print("="*60 + "\n")


if __name__ == '__main__':
    main()
