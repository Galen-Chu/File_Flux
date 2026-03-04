"""
Abstract base class for storage backends
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class FileInfo:
    """Data class representing file information"""
    name: str
    path: str
    size: int
    modified_time: datetime
    source: str  # 'local' or 's3'
    is_directory: bool = False
    content_type: Optional[str] = None
    etag: Optional[str] = None  # S3-specific

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'source': self.source,
            'is_directory': self.is_directory,
            'content_type': self.content_type,
            'etag': self.etag,
        }


class BaseStorage(ABC):
    """Abstract base class for storage backends"""

    @abstractmethod
    def list_files(self, path: str = '') -> List[FileInfo]:
        """
        List files in the given path

        Args:
            path: Path to list files from (relative to storage root)

        Returns:
            List of FileInfo objects
        """
        pass

    @abstractmethod
    def rename_files(self, files: List[str], text: str, mode: str = 'prefix',
                     add_sequence: bool = False, start_number: int = 1,
                     find_text: Optional[str] = None, case_sensitive: bool = False,
                     use_regex: bool = False, replace_all: bool = True) -> dict:
        """
        Rename files by adding prefix/suffix or replacing text

        Args:
            files: List of file paths to rename
            text: Text to add as prefix/suffix or replacement text
            mode: 'prefix', 'suffix', or 'replace'
            add_sequence: Whether to add sequential numbering
            start_number: Starting number for sequence

            Replace mode specific:
            find_text: Text to find and replace (required for replace mode)
            case_sensitive: Case-sensitive matching (default: False)
            use_regex: Treat find_text as regex (default: False)
            replace_all: Replace all occurrences or just first (default: True)

        Returns:
            Dictionary with 'success' list and 'failed' list with error messages
        """
        pass

    @abstractmethod
    def delete_files(self, files: List[str]) -> dict:
        """
        Delete specified files

        Args:
            files: List of file paths to delete

        Returns:
            Dictionary with 'success' list and 'failed' list with error messages
        """
        pass

    @abstractmethod
    def upload_file(self, source_path: str, dest_path: str) -> bool:
        """
        Upload a file to storage

        Args:
            source_path: Local source file path
            dest_path: Destination path in storage

        Returns:
            True if successful

        Raises:
            FileOperationError: If upload fails
        """
        pass

    @abstractmethod
    def download_file(self, source_path: str, dest_path: str) -> bool:
        """
        Download a file from storage

        Args:
            source_path: Source path in storage
            dest_path: Local destination file path

        Returns:
            True if successful

        Raises:
            FileOperationError: If download fails
        """
        pass

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists

        Args:
            path: File path to check

        Returns:
            True if file exists
        """
        pass

    @abstractmethod
    def get_file_info(self, path: str) -> Optional[FileInfo]:
        """
        Get information about a specific file

        Args:
            path: File path

        Returns:
            FileInfo object if file exists, None otherwise
        """
        pass
