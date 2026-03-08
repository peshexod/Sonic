import boto3
import os
from typing import Optional


def upload_to_storage(
    file_path: str,
    endpoint: str,
    bucket: str,
    access_key: str,
    secret_key: str,
    object_name: Optional[str] = None
) -> str:
    """
    Upload file to S3-compatible storage.
    
    Args:
        file_path: Path to file to upload
        endpoint: S3 endpoint URL
        bucket: Bucket name
        access_key: Access key
        secret_key: Secret key
        object_name: Optional object name (defaults to filename)
        
    Returns:
        url: Public URL of uploaded file
    """
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    # Create S3 client
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    # Upload file
    s3_client.upload_file(
        file_path,
        bucket,
        object_name,
        ExtraArgs={'ContentType': 'video/mp4'}
    )
    
    # Construct public URL
    # Try to determine URL format based on endpoint
    if 'storage.googleapis.com' in endpoint or 'googleapis.com' in endpoint:
        url = f"https://{bucket}.storage.googleapis.com/{object_name}"
    elif 'digitaloceanspaces.com' in endpoint or 'do-spaces' in endpoint:
        url = f"https://{bucket}.{endpoint.replace('https://', '')}/{object_name}"
    else:
        # Default S3 URL format
        url = f"{endpoint}/{bucket}/{object_name}"
    
    return url
