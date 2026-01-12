"""S3 service for image upload."""
import boto3
from botocore.exceptions import ClientError
from app.config import settings
import logging
from typing import Optional
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class S3Service:
    """Service for AWS S3 operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        self.bucket = settings.s3_bucket
        self.region = settings.aws_region
        
        # Initialize S3 client
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=self.region
            )
        else:
            # Use IAM role or environment credentials
            self.s3_client = boto3.client('s3', region_name=self.region)
    
    def upload_file(self, file_content: bytes, product_id: int, file_extension: str) -> str:
        """
        Upload file to S3.
        
        Args:
            file_content: File content as bytes
            product_id: Product ID
            file_extension: File extension (e.g., 'jpg', 'png')
        
        Returns:
            str: Public URL of uploaded file
        
        Raises:
            Exception: If upload fails
        """
        try:
            # Generate S3 key
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            key = f"products/{product_id}/{timestamp}.{file_extension}"
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_content,
                ContentType=f"image/{file_extension}",
                ACL='public-read'
            )
            
            # Generate public URL
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
            logger.info(f"File uploaded successfully to {url}")
            return url
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            raise Exception(f"Failed to upload file to S3: {str(e)}")
    
    def delete_file(self, file_url: str) -> bool:
        """
        Delete file from S3.
        
        Args:
            file_url: Full URL of the file
        
        Returns:
            bool: True if deletion successful
        """
        try:
            # Extract key from URL
            # Format: https://bucket.s3.region.amazonaws.com/key
            if not file_url:
                return True
                
            parts = file_url.split('.amazonaws.com/')
            if len(parts) < 2:
                logger.warning(f"Invalid S3 URL format: {file_url}")
                return False
            
            key = parts[1]
            
            # Delete file
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"File deleted successfully from S3: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"S3 deletion failed: {e}")
            return False
    
    def check_connection(self) -> bool:
        """
        Check S3 connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket)
            return True
        except ClientError as e:
            logger.error(f"S3 connection check failed: {e}")
            return False


# Create singleton instance
s3_service = S3Service()
