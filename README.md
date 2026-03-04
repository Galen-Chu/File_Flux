# FileFlux - Unified Cloud File Manager

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](./VERSION.md)
[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14+-brightgreen.svg)](https://www.python.org/)

A modern Django-based file management application with unified control over local storage and AWS S3, featuring a responsive web interface and comprehensive REST API.

## ✨ Key Features

### Core Functionality
- 📁 **Unified File Management** - Single interface for local and AWS S3 storage
- 🔄 **Bulk Operations** - Multi-file selection for rename, delete, and move operations
- 🚀 **REST API** - Complete RESTful API with Django REST Framework
- 🎨 **Modern UI** - Responsive web interface with Tailwind CSS
- 📝 **Audit Logging** - Track all file operations with timestamps

### Enhanced Rename Features (v1.1.0)
- 🏷️ **Prefix/Suffix Mode** - Choose to add text before or after filenames
- 🔢 **Sequential Numbering** - Add zero-padded sequence numbers (001, 002, 003...)
- ⚙️ **Configurable Options** - Set custom starting numbers for sequences
- 🎯 **Smart Extension Handling** - Extensions preserved correctly in all operations

### Technical Features
- 🏗️ **Service Layer Architecture** - Strategy pattern with abstract storage interface
- 🔒 **Security First** - Path validation, file size limits, input sanitization
- 📊 **Pagination** - Efficient handling of large file lists
- 🌐 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🌍 **S3 Compatible** - Works with any S3-compatible storage (MinIO, DigitalOcean Spaces, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher
- pip package manager
- AWS account (for S3 features)

### Installation

1. **Navigate to project directory**
   ```bash
   cd D:\FileFlux
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Configure environment variables**
   ```bash
   cp .env.template .env
   ```

   Edit `.env` with your credentials:
   ```env
   # AWS Credentials
   AWS_ACCESS_KEY=your_aws_access_key
   AWS_SECRET_KEY=your_aws_secret_key
   BUCKET_NAME=your_s3_bucket_name
   AWS_REGION=us-east-1

   # Storage Configuration
   LOCAL_STORAGE_PATH=D:\FileFlux\storage
   MAX_UPLOAD_SIZE_MB=100
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main page: http://127.0.0.1:8000/
   - File Manager: http://127.0.0.1:8000/manager/
   - API Browser: http://127.0.0.1:8000/api/files/

## 📖 Usage Examples

### Using the Web Interface

1. **Navigate to File Manager**
   - Go to http://127.0.0.1:8000/manager/
   - Use tabs to filter by source (All, Local, S3)

2. **Bulk Rename Files**
   - Select multiple files using checkboxes
   - Click "Rename Selected"
   - Choose mode: Prefix or Suffix
   - Enter text (e.g., `backup_` or `_final`)
   - Optionally enable sequential numbering
   - Click "Rename"

3. **Upload Files**
   - Click "Upload" button
   - Select file from your computer
   - Optionally specify destination path
   - File uploads to S3

4. **Download Files**
   - Find S3 file in the list
   - Click "Download" button
   - File saves to local storage directory

### Using the REST API

**List Files:**
```bash
# List all files
curl http://127.0.0.1:8000/api/files/

# List only local files
curl "http://127.0.0.1:8000/api/files/?source=local"

# List only S3 files
curl "http://127.0.0.1:8000/api/files/?source=s3"
```

**Bulk Rename with Enhanced Features:**
```bash
# Prefix mode with sequential numbering
curl -X POST http://127.0.0.1:8000/api/files/rename/ \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["doc1.txt", "doc2.txt", "doc3.txt"],
    "text": "file_",
    "mode": "prefix",
    "add_sequence": true,
    "start_number": 1,
    "source": "local"
  }'
# Result: file_doc1_001.txt, file_doc2_002.txt, file_doc3_003.txt

# Suffix mode without sequence
curl -X POST http://127.0.0.1:8000/api/files/rename/ \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["report.pdf"],
    "text": "_backup",
    "mode": "suffix",
    "add_sequence": false,
    "source": "s3"
  }'
# Result: report_backup.pdf
```

**Upload File:**
```bash
curl -X POST http://127.0.0.1:8000/api/files/upload/ \
  -F "file=@local_file.txt" \
  -F "dest_path=uploads/remote_file.txt"
```

**Download File:**
```bash
curl -X POST http://127.0.0.1:8000/api/files/download/ \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "documents/report.pdf",
    "dest_path": "D:\\FileFlux\\storage\\report.pdf"
  }'
```

**Delete Files:**
```bash
curl -X POST http://127.0.0.1:8000/api/files/delete/ \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["old_file1.txt", "old_file2.txt"],
    "source": "local"
  }'
```

**View Operation Logs:**
```bash
curl "http://127.0.0.1:8000/api/files/logs/?limit=10"
```

## 📁 Project Structure

```
file_flux/
├── file_flux/              # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI application
│
├── manager/                # Main application
│   ├── services/          # Storage service layer
│   │   ├── base.py        # Abstract BaseStorage interface
│   │   ├── local_storage.py   # Local filesystem backend
│   │   ├── s3_storage.py  # AWS S3 backend
│   │   ├── unified_storage.py # Unified storage manager
│   │   ├── exceptions.py  # Custom exceptions
│   │   └── __init__.py    # Factory functions
│   │
│   ├── models.py          # FileOperation audit model
│   ├── serializers.py     # DRF serializers
│   ├── api_views.py       # REST API views
│   ├── api_urls.py        # API URL routing
│   ├── views.py           # Frontend views
│   └── urls.py            # App URL routing
│
├── templates/              # HTML templates
│   ├── index.html         # Landing page
│   └── file_manager.html  # File manager UI
│
├── storage/               # Local file storage directory
│
├── venv/                  # Virtual environment
│
├── .env                   # Environment variables (create from .env.template)
├── .env.template         # Environment variables template
├── .gitignore            # Git ignore file
├── manage.py             # Django management script
│
├── README.md             # This file
├── VERSION.md            # Version information
├── CHANGELOG.md          # Detailed changelog
└── IMPLEMENTATION_PLAN.md # Technical documentation
```

## 🏗️ Architecture

### Service Layer Pattern

FileFlux uses a **Strategy Pattern** with abstract base classes for storage backends:

```
BaseStorage (Abstract)
    ├── LocalStorage (Local filesystem)
    ├── S3Storage (AWS S3)
    └── UnifiedStorage (Aggregates both)
```

**Benefits:**
- Easy to add new storage backends
- Consistent interface across all storage types
- Separation of concerns
- Testable architecture

### Key Components

**1. Service Layer (`manager/services/`)**
- Abstract storage interface
- Business logic for file operations
- Error handling and validation
- Storage-specific implementations

**2. API Layer (`manager/api_views.py`)**
- RESTful endpoints
- Request validation
- Response formatting
- Operation logging

**3. Frontend (`templates/file_manager.html`)**
- Responsive UI with Tailwind CSS
- Vanilla JavaScript
- Fetch API for HTTP requests
- Real-time updates

**4. Database (`manager/models.py`)**
- Audit logging
- Operation tracking
- SQLite for development

## 🔌 API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/files/` | GET | List files (supports source filtering) |
| `/api/files/rename/` | POST | Bulk rename files (prefix/suffix + sequence) |
| `/api/files/delete/` | POST | Bulk delete files |
| `/api/files/upload/` | POST | Upload file to S3 |
| `/api/files/download/` | POST | Download file from S3 |
| `/api/files/logs/` | GET | View operation audit logs |

For detailed API documentation, see [PLAN_v1.0.0_initial_implementation.md](./PLAN_v1.0.0_initial_implementation.md)

## 🛠️ Development

### Creating Migrations

If you modify models, create migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`

### Running Tests

```bash
python manage.py test
```

## 📦 Installed Packages

- **django** (6.0.2) - Web framework
- **djangorestframework** (3.16.1) - REST API framework
- **boto3** (1.42.59) - AWS SDK for Python
- **python-dotenv** (1.2.2) - Environment variable management

## 📚 Documentation

- [VERSION.md](./VERSION.md) - Version information and upgrade guide
- [CHANGELOG.md](./CHANGELOG.md) - Detailed changelog
- [PLAN_v1.0.0_initial_implementation.md](./PLAN_v1.0.0_initial_implementation.md) - Technical documentation and API reference
- [PLAN_v1.2.0_replace_mode.md](./PLAN_v1.2.0_replace_mode.md) - Replace mode feature plan
- [PLAN_v2.0.0_cloud_drive.md](./PLAN_v2.0.0_cloud_drive.md) - Cloud drive integration plan
- [PLAN_roadmap_future_features.md](./PLAN_roadmap_future_features.md) - Feature roadmap and future plans

## 🔒 Security Considerations

**Current Implementation (Development Mode):**
- ⚠️ No authentication (suitable for development only)
- ⚠️ No rate limiting
- ✅ Path validation to prevent directory traversal
- ✅ File size validation
- ✅ Input sanitization

**For Production:**
- Add authentication (TokenAuthentication or SessionAuthentication)
- Implement rate limiting
- Add HTTPS
- Enable Django security settings
- Use environment-based secrets management
- Review and update security settings

See [PLAN_v1.0.0_initial_implementation.md](./PLAN_v1.0.0_initial_implementation.md) for detailed security guidelines.

## 🐛 Troubleshooting

### Common Issues

**AWS Credentials Not Found**
```
Error: NoCredentialsError
Solution: Check .env file has AWS_ACCESS_KEY and AWS_SECRET_KEY
```

**S3 Bucket Not Accessible**
```
Error: ClientError - AccessDenied
Solution: Verify bucket name and AWS permissions
```

**Local Storage Path Not Found**
```
Error: FileNotFoundError
Solution: Create D:\FileFlux\storage directory
```

**File Upload Fails**
```
Error: RequestDataTooBig
Solution: Increase MAX_UPLOAD_SIZE_MB in .env
```

For more troubleshooting help, see [PLAN_v1.0.0_initial_implementation.md](./PLAN_v1.0.0_initial_implementation.md)

## 🗺️ Roadmap

### Upcoming Features
- [ ] File preview for images and PDFs
- [ ] Search and filter functionality
- [ ] Drag & drop file upload
- [ ] Bi-directional sync between local and S3
- [ ] File versioning support
- [ ] Real-time updates via WebSocket

See [VERSION.md](./VERSION.md) for detailed roadmap.

## 🤝 Contributing

This project is currently in active development. Contributions, issues, and feature requests are welcome!

## 📄 License

This project is for educational and development purposes.

---

**Current Version:** 1.1.0
**Last Updated:** 2026-03-03
**Maintained By:** FileFlux Development Team
