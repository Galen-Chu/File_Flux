"""
Custom exceptions for file operations
"""


class FileOperationError(Exception):
    """Base exception for file operations"""

    def __init__(self, message, operation=None, file_path=None, original_error=None):
        self.message = message
        self.operation = operation
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.operation:
            parts.insert(0, f"[{self.operation}]")
        if self.file_path:
            parts.append(f"File: {self.file_path}")
        if self.original_error:
            parts.append(f"Error: {str(self.original_error)}")
        return " | ".join(parts)


class FileNotFoundError(FileOperationError):
    """Raised when a file is not found"""

    def __init__(self, file_path, operation=None):
        super().__init__(
            message=f"File not found: {file_path}",
            operation=operation,
            file_path=file_path
        )


class PermissionDeniedError(FileOperationError):
    """Raised when permission is denied for file operation"""

    def __init__(self, file_path, operation=None):
        super().__init__(
            message=f"Permission denied: {file_path}",
            operation=operation,
            file_path=file_path
        )


class StorageConnectionError(FileOperationError):
    """Raised when unable to connect to storage backend"""

    def __init__(self, message, storage_type=None, original_error=None):
        self.storage_type = storage_type
        super().__init__(
            message=message,
            original_error=original_error
        )


class InvalidPathError(FileOperationError):
    """Raised when file path is invalid or contains forbidden characters"""

    def __init__(self, file_path, reason=None):
        message = f"Invalid path: {file_path}"
        if reason:
            message += f" - {reason}"
        super().__init__(
            message=message,
            file_path=file_path
        )


class FileSizeExceededError(FileOperationError):
    """Raised when file size exceeds maximum allowed"""

    def __init__(self, file_size, max_size, file_path=None):
        self.file_size = file_size
        self.max_size = max_size
        super().__init__(
            message=f"File size ({file_size} bytes) exceeds maximum ({max_size} bytes)",
            file_path=file_path
        )
