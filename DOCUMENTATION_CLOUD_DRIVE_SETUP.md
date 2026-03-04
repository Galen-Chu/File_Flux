# Cloud Drive Setup Guide

This guide explains how to configure Microsoft OneDrive and Google Drive integration in FileFlux.

---

## Current Implementation Status

**v2.0.0** includes:
- ✅ User authentication system
- ✅ CloudStorageToken model for OAuth tokens
- ✅ Cloud drive connection UI
- ✅ Demo mode for testing
- ⏳ Full OAuth implementation (requires cloud provider credentials)

---

## Demo Mode

The current implementation includes a **demo mode** that allows you to test the cloud drive connection UI without setting up actual OAuth credentials.

### Testing Demo Mode

1. Log in to FileFlux
2. Navigate to your Profile (click the gear icon in the header)
3. Click "Connect OneDrive" or "Connect Google Drive"
4. The demo mode will simulate a successful connection

This allows you to:
- See how connected drives appear in the profile
- Test the disconnect functionality
- Understand the UI flow

---

## Production Setup

For production use with real cloud drives, you need to configure OAuth credentials.

### Microsoft OneDrive Setup

#### Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: FileFlux
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: Web - `http://localhost:8000/oauth/callback/` (update for production)
5. Click **Register**

#### Step 2: Get Credentials

1. In your app overview, copy the **Application (client) ID**
2. Go to **Certificates & secrets** → **New client secret**
3. Add a description and expiry, then click **Add**
4. Copy the secret value (you won't see it again!)

#### Step 3: Configure Permissions

1. Go to **API permissions** → **Add a permission**
2. Select **Microsoft Graph** → **Delegated permissions**
3. Search for and add:
   - `Files.ReadWrite.All`
   - `offline_access`
4. Click **Add permissions**

#### Step 4: Update .env

```bash
MS_CLIENT_ID=your_application_client_id_here
MS_CLIENT_SECRET=your_client_secret_here
MS_TENANT_ID=common  # or your specific tenant ID
```

---

### Google Drive Setup

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Drive API**:
   - Go to **APIs & Services** → **Library**
   - Search for "Google Drive API"
   - Click **Enable**

#### Step 2: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure the consent screen first:
   - Choose **External** user type
   - Fill in required fields (app name, email)
   - Add scopes: `https://www.googleapis.com/auth/drive.file`
   - Add test users (your email)
4. For OAuth client:
   - **Application type**: Web application
   - **Name**: FileFlux
   - **Authorized redirect URIs**: `http://localhost:8000/oauth/callback/`
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

#### Step 3: Update .env

```bash
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

---

## OAuth Callback Handler

The redirect URI (`http://localhost:8000/oauth/callback/`) needs to be implemented to handle the OAuth callback and exchange authorization codes for tokens.

### Current Status

The callback handler is **not yet implemented** in v2.0.0. For full OAuth support, you need to:

1. Create an OAuth callback view
2. Exchange authorization code for tokens
3. Store tokens in CloudStorageToken model
4. Implement token refresh logic

### Future Implementation

Full OAuth implementation is planned for a future version. The current infrastructure supports:

- Token storage (CloudStorageToken model)
- Token expiration checking
- Connection status display
- Disconnect functionality

---

## Security Considerations

### HTTPS Requirement

⚠️ **OAuth requires HTTPS in production**

- Use HTTPS for all OAuth redirects
- Update `OAUTH_REDIRECT_URI` to use `https://`
- Configure secure cookies in Django settings

### Token Storage

Tokens are currently stored in plain text in the database. For production:

1. **Encrypt tokens at rest**:
   ```python
   from cryptography.fernet import Fernet

   # Generate encryption key
   key = Fernet.generate_key()

   # In CloudStorageToken model
   def set_access_token(self, token):
       f = Fernet(settings.ENCRYPTION_KEY)
       self.access_token = f.encrypt(token.encode())

   def get_access_token(self):
       f = Fernet(settings.ENCRYPTION_KEY)
       return f.decrypt(self.access_token).decode()
   ```

2. **Use environment variables** for all credentials
3. **Never commit** .env file to version control

---

## Alternative: Rclone Integration

Instead of implementing OAuth from scratch, consider using **Rclone**:

### Benefits
- ✅ 40+ cloud providers supported
- ✅ Handles OAuth automatically
- ✅ Battle-tested and maintained
- ✅ Token refresh built-in

### Installation

```bash
pip install rclone-python
```

### Configuration

1. Install rclone binary: https://rclone.org/install/
2. Configure remote: `rclone config`
3. Use rclone Python wrapper in storage backend

### Recommendation

For faster implementation with broader provider support, **Rclone is recommended** over native OAuth.

---

## Testing Cloud Drives

### Without Credentials (Demo Mode)

```bash
# Start server
python manage.py runserver

# Visit http://localhost:8000/register/
# Create account
# Go to Profile
# Click "Connect OneDrive?demo=true"
```

### With Credentials (Production)

1. Configure OAuth credentials in `.env`
2. Implement OAuth callback handler
3. Test authentication flow
4. Verify token storage
5. Test file operations

---

## Troubleshooting

### "Invalid redirect URI" Error
- Ensure redirect URI matches exactly in Azure/Google Console
- Check for trailing slashes
- Verify http vs https

### "Access denied" Error
- Check API permissions are granted
- Verify consent screen is configured
- Ensure scopes are correct

### Token Expiration
- Implement token refresh logic
- Check `offline_access` scope is requested
- Monitor `token_expires_at` field

---

## Next Steps

1. **For development**: Use demo mode to test UI
2. **For production**:
   - Set up OAuth credentials
   - Implement callback handler
   - Add token encryption
   - Configure HTTPS

3. **Alternative approach**: Integrate Rclone for faster implementation

---

## Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Google Drive API Documentation](https://developers.google.com/drive)
- [Rclone Documentation](https://rclone.org/docs/)
- [OAuth 2.0 RFC](https://oauth.net/2/)

---

**Version**: 2.0.0
**Last Updated**: 2026-03-03
