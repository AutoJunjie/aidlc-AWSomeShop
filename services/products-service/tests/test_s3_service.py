"""Unit tests for S3 service."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from app.services.s3_service import S3Service


class TestS3Service:
    """Test cases for S3Service."""
    
    @patch('app.services.s3_service.boto3.client')
    def test_init_with_credentials(self, mock_boto_client):
        """Test S3Service initialization with credentials."""
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.aws_access_key_id = "test_key"
            mock_settings.aws_secret_access_key = "test_secret"
            mock_settings.aws_region = "us-east-1"
            mock_settings.s3_bucket = "test-bucket"
            
            service = S3Service()
            
            mock_boto_client.assert_called_once_with(
                's3',
                aws_access_key_id="test_key",
                aws_secret_access_key="test_secret",
                region_name="us-east-1"
            )
    
    @patch('app.services.s3_service.boto3.client')
    def test_init_without_credentials(self, mock_boto_client):
        """Test S3Service initialization without credentials (uses IAM role)."""
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            mock_settings.aws_region = "us-west-2"
            mock_settings.s3_bucket = "test-bucket"
            
            service = S3Service()
            
            mock_boto_client.assert_called_once_with('s3', region_name="us-west-2")
    
    @patch('app.services.s3_service.boto3.client')
    def test_upload_file_success(self, mock_boto_client):
        """Test successful file upload."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            file_content = b"test image content"
            product_id = 123
            file_extension = "jpg"
            
            result = service.upload_file(file_content, product_id, file_extension)
            
            # Verify put_object was called
            mock_s3.put_object.assert_called_once()
            call_args = mock_s3.put_object.call_args
            
            assert call_args[1]['Bucket'] == "test-bucket"
            assert call_args[1]['Body'] == file_content
            assert call_args[1]['ContentType'] == "image/jpg"
            assert call_args[1]['ACL'] == 'public-read'
            assert f"products/{product_id}/" in call_args[1]['Key']
            assert call_args[1]['Key'].endswith(".jpg")
            
            # Verify URL format
            assert result.startswith(f"https://test-bucket.s3.us-east-1.amazonaws.com/products/{product_id}/")
            assert result.endswith(".jpg")
    
    @patch('app.services.s3_service.boto3.client')
    def test_upload_file_failure(self, mock_boto_client):
        """Test file upload failure."""
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = ClientError(
            {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}},
            'PutObject'
        )
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            with pytest.raises(Exception) as exc_info:
                service.upload_file(b"content", 1, "jpg")
            
            assert "Failed to upload file to S3" in str(exc_info.value)
    
    @patch('app.services.s3_service.boto3.client')
    def test_delete_file_success(self, mock_boto_client):
        """Test successful file deletion."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            file_url = "https://test-bucket.s3.us-east-1.amazonaws.com/products/123/test.jpg"
            
            result = service.delete_file(file_url)
            
            assert result is True
            mock_s3.delete_object.assert_called_once_with(
                Bucket="test-bucket",
                Key="products/123/test.jpg"
            )
    
    @patch('app.services.s3_service.boto3.client')
    def test_delete_file_invalid_url(self, mock_boto_client):
        """Test deletion with invalid URL."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            result = service.delete_file("https://invalid-url.com/file.jpg")
            
            assert result is False
            mock_s3.delete_object.assert_not_called()
    
    @patch('app.services.s3_service.boto3.client')
    def test_delete_file_empty_url(self, mock_boto_client):
        """Test deletion with empty URL."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            result = service.delete_file("")
            
            assert result is True  # Returns True for empty URL
            mock_s3.delete_object.assert_not_called()
    
    @patch('app.services.s3_service.boto3.client')
    def test_delete_file_failure(self, mock_boto_client):
        """Test file deletion failure."""
        mock_s3 = MagicMock()
        mock_s3.delete_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'The specified key does not exist'}},
            'DeleteObject'
        )
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            result = service.delete_file("https://test-bucket.s3.us-east-1.amazonaws.com/products/1/test.jpg")
            
            assert result is False
    
    @patch('app.services.s3_service.boto3.client')
    def test_check_connection_success(self, mock_boto_client):
        """Test successful connection check."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            result = service.check_connection()
            
            assert result is True
            mock_s3.head_bucket.assert_called_once_with(Bucket="test-bucket")
    
    @patch('app.services.s3_service.boto3.client')
    def test_check_connection_failure(self, mock_boto_client):
        """Test connection check failure."""
        mock_s3 = MagicMock()
        mock_s3.head_bucket.side_effect = ClientError(
            {'Error': {'Code': '404', 'Message': 'Not Found'}},
            'HeadBucket'
        )
        mock_boto_client.return_value = mock_s3
        
        with patch('app.services.s3_service.settings') as mock_settings:
            mock_settings.s3_bucket = "test-bucket"
            mock_settings.aws_region = "us-east-1"
            mock_settings.aws_access_key_id = None
            mock_settings.aws_secret_access_key = None
            
            service = S3Service()
            
            result = service.check_connection()
            
            assert result is False
