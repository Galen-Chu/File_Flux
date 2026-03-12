"""
Cloud Drive API Views

API endpoints for Google Drive and OneDrive operations
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CloudStorageToken, FileOperation
from .services.google_drive_service import GoogleDriveService


class CloudDriveViewSet(viewsets.ViewSet):
    """ViewSet for cloud drive operations"""

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='files')
    def list_files(self, request):
        """
        List files from connected cloud drive

        Query params:
            - provider: 'googledrive' or 'onedrive'
            - folder_id: folder ID to list (optional, defaults to root)
            - page_size: number of files per page (default 50)
            - page_token: pagination token
            - query: search query (optional)
        """
        provider = request.query_params.get('provider', 'googledrive')

        # Get user's token for this provider
        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.list_files(
                page_size=int(request.query_params.get('page_size', 50)),
                page_token=request.query_params.get('page_token'),
                folder_id=request.query_params.get('folder_id'),
                query=request.query_params.get('query')
            )

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                'files': result['files'],
                'next_page_token': result.get('next_page_token'),
                'provider': provider
            })

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='files/(?P<file_id>[^/.]+)')
    def get_file(self, request, file_id=None):
        """
        Get file metadata from cloud drive

        Query params:
            - provider: 'googledrive' or 'onedrive'
        """
        provider = request.query_params.get('provider', 'googledrive')

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.get_file(file_id)

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(result)

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_file(self, request):
        """
        Upload file to cloud drive

        Request body (multipart/form-data):
            - file: file to upload
            - provider: 'googledrive' or 'onedrive'
            - parent_folder_id: folder ID to upload to (optional)
        """
        provider = request.data.get('provider', 'googledrive')

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.upload_file(
                file_content=uploaded_file.read(),
                filename=uploaded_file.name,
                mime_type=uploaded_file.content_type,
                parent_folder_id=request.data.get('parent_folder_id')
            )

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the operation
            FileOperation.objects.create(
                operation='UPLOAD',
                source=provider,
                file_path=result['name'],
                success=True,
                file_size=result['size']
            )

            return Response(result, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='download')
    def download_file(self, request):
        """
        Download file from cloud drive

        Request body (JSON):
            - file_id: ID of file to download
            - provider: 'googledrive' or 'onedrive'
        """
        provider = request.data.get('provider', 'googledrive')
        file_id = request.data.get('file_id')

        if not file_id:
            return Response(
                {'error': 'file_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.download_file(file_id)

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Return file as download
            from django.http import HttpResponse
            response = HttpResponse(
                result['content'],
                content_type=result['mime_type']
            )
            response['Content-Disposition'] = f'attachment; filename="{result["name"]}"'

            # Log the operation
            FileOperation.objects.create(
                operation='DOWNLOAD',
                source=provider,
                file_path=result['name'],
                success=True,
                file_size=result['size']
            )

            return response

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='create-folder')
    def create_folder(self, request):
        """
        Create folder in cloud drive

        Request body (JSON):
            - name: folder name
            - provider: 'googledrive' or 'onedrive'
            - parent_folder_id: parent folder ID (optional)
        """
        provider = request.data.get('provider', 'googledrive')
        folder_name = request.data.get('name')

        if not folder_name:
            return Response(
                {'error': 'name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.create_folder(
                folder_name=folder_name,
                parent_folder_id=request.data.get('parent_folder_id')
            )

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(result, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['delete'], url_path='files/(?P<file_id>[^/.]+)')
    def delete_file(self, request, file_id=None):
        """
        Delete file from cloud drive

        Query params:
            - provider: 'googledrive' or 'onedrive'
        """
        provider = request.query_params.get('provider', 'googledrive')

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.delete_file(file_id)

            if not result.get('success'):
                return Response(
                    {'error': result.get('error', 'Delete failed')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the operation
            FileOperation.objects.create(
                operation='DELETE',
                source=provider,
                file_path=file_id,
                success=True
            )

            return Response({'success': True, 'message': 'File deleted'})

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='files/(?P<file_id>[^/.]+)/rename')
    def rename_file(self, request, file_id=None):
        """
        Rename file in cloud drive

        Request body (JSON):
            - new_name: new filename
            - provider: 'googledrive' or 'onedrive'
        """
        provider = request.data.get('provider', 'googledrive')
        new_name = request.data.get('new_name')

        if not new_name:
            return Response(
                {'error': 'new_name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = CloudStorageToken.objects.get(
                user=request.user,
                provider=provider
            )
        except CloudStorageToken.DoesNotExist:
            return Response(
                {'error': f'{provider} is not connected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == 'googledrive':
            service = GoogleDriveService(token)
            result = service.rename_file(file_id, new_name)

            if result.get('error'):
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the operation
            FileOperation.objects.create(
                operation='RENAME',
                source=provider,
                file_path=result['name'],
                success=True
            )

            return Response(result)

        else:
            return Response(
                {'error': f'Provider {provider} not yet supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
