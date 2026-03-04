"""
Unified storage service that aggregates multiple backends
"""
from typing import List, Optional, Dict

from .base import BaseStorage, FileInfo
from .local_storage import LocalStorage
from .s3_storage import S3Storage
from .exceptions import FileOperationError


class UnifiedStorage:
    """
    Unified storage manager that aggregates local and S3 storage backends
    """

    def __init__(self, local_storage: LocalStorage, s3_storage: S3Storage):
        """
        Initialize unified storage

        Args:
            local_storage: Local storage backend
            s3_storage: S3 storage backend
        """
        self.local_storage = local_storage
        self.s3_storage = s3_storage

    def list_files(self, source: Optional[str] = None, path: str = '') -> List[FileInfo]:
        """
        List files from specified source or all sources

        Args:
            source: Optional source filter ('local', 's3', or None for all)
            path: Path to list files from

        Returns:
            List of FileInfo objects
        """
        files = []

        try:
            if source is None or source == 'local':
                local_files = self.local_storage.list_files(path)
                files.extend(local_files)

            if source is None or source == 's3':
                s3_files = self.s3_storage.list_files(path)
                files.extend(s3_files)

            # Sort by name
            files.sort(key=lambda x: (x.source, x.name))

        except Exception as e:
            raise FileOperationError(
                f"Failed to list files from unified storage",
                operation='list',
                original_error=e
            )

        return files

    def rename_files(self, files: List[str], text: str, source: str,
                     mode: str = 'prefix', add_sequence: bool = False,
                     start_number: int = 1, find_text: Optional[str] = None,
                     case_sensitive: bool = False, use_regex: bool = False,
                     replace_all: bool = True) -> dict:
        """
        Rename files in specified storage backend

        Args:
            files: List of file paths to rename
            text: Text to add as prefix or suffix
            source: Storage source ('local' or 's3')
            mode: 'prefix' or 'suffix'
            add_sequence: Whether to add sequential numbering
            start_number: Starting number for sequence

        Returns:
            Dict with 'success' and 'failed' lists
        """
        if source == 'local':
            return self.local_storage.rename_files(
                files, text, mode, add_sequence, start_number,
                find_text, case_sensitive, use_regex, replace_all
            )
        elif source == 's3':
            return self.s3_storage.rename_files(
                files, text, mode, add_sequence, start_number,
                find_text, case_sensitive, use_regex, replace_all
            )
        else:
            return {
                'success': [],
                'failed': [{'file': f, 'error': f'Invalid source: {source}'} for f in files]
            }

    def delete_files(self, files: List[str], source: str) -> dict:
        """
        Delete files from specified storage backend

        Args:
            files: List of file paths to delete
            source: Storage source ('local' or 's3')

        Returns:
            Dict with 'success' and 'failed' lists
        """
        if source == 'local':
            return self.local_storage.delete_files(files)
        elif source == 's3':
            return self.s3_storage.delete_files(files)
        else:
            return {
                'success': [],
                'failed': [{'file': f, 'error': f'Invalid source: {source}'} for f in files]
            }

    def upload_file(self, source_path: str, dest_path: str) -> bool:
        """
        Upload file to S3 (from local filesystem to S3)

        Args:
            source_path: Local source file path
            dest_path: S3 destination path

        Returns:
            True if successful
        """
        return self.s3_storage.upload_file(source_path, dest_path)

    def download_file(self, source_path: str, dest_path: str) -> bool:
        """
        Download file from S3 (from S3 to local filesystem)

        Args:
            source_path: S3 source path
            dest_path: Local destination path

        Returns:
            True if successful
        """
        return self.s3_storage.download_file(source_path, dest_path)

    def get_storage(self, source: str) -> Optional[BaseStorage]:
        """
        Get storage backend by source

        Args:
            source: Storage source ('local' or 's3')

        Returns:
            Storage backend or None if invalid source
        """
        if source == 'local':
            return self.local_storage
        elif source == 's3':
            return self.s3_storage
        return None

    def file_exists(self, path: str, source: str) -> bool:
        """
        Check if file exists in specified backend

        Args:
            path: File path
            source: Storage source ('local' or 's3')

        Returns:
            True if file exists
        """
        storage = self.get_storage(source)
        if storage:
            return storage.file_exists(path)
        return False

    def get_file_info(self, path: str, source: str) -> Optional[FileInfo]:
        """
        Get information about a file

        Args:
            path: File path
            source: Storage source ('local' or 's3')

        Returns:
            FileInfo if exists, None otherwise
        """
        storage = self.get_storage(source)
        if storage:
            return storage.get_file_info(path)
        return None
