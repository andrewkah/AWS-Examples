import boto3
from botocore.exceptions import ClientError
import json
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')

def create_multipart_upload(bucket_name, object_key):
    """ Initiate the upload to return an Upload ID"""
    try:
        response = s3.create_multipart_upload(Bucket=bucket_name, Key=object_key)
        print(response['Upload-ID'])
        return response
    except ClientError as e:
        print(f"Failed to create multipart upload: {e}")
        
def upload_part(bucket_name, object_key, body, upload_id):
    """ Upload the first upload part to create the Etag for the next upload
    """
    try:
        response = s3.upload_part(Bucket=bucket_name, Key=object_key, PartNumber=1, Body=body, UploadId=upload_id)
        print(response)
        return response
    except ClientError as e:
        print(f"Failed to upload the first part: {e}")
        
def resolve_upload_ids_to_etags(new_etag, new_id, bucket_name):
    """ Organise the upload file into a proper json
    """
    new_dict = {"PartNumber": new_id, "Etag": new_etag}
    file_path = Path(f"{bucket_name}.json")
    if file_path.exists() and file_path.stat().st_size > 0:
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    data["Parts"] = [data]
        except json.JSONDecodeError as jsone:
            data = []
    else:
        data = []
    
    data["Parts"].append(new_dict)
    
    with open(file_path, "a+", encoding="utf-8"):
        json.dump(data, f, indent=2)

def complete_multipart_upload(bucket_name, object_key, upload_file, upload_id):
    """ Upload the corresponding parts of the multi parts
    """
    try:
        print("Please wait...")
        response = s3.complete_multipart_upload(Bucket=bucket_name, Key=object_key, MultipartUpload=upload_file, UploadId=upload_id)
        print(response)
        return response
    except ClientError as e:
        print(f"Failed to complete multipart upload: {e}")
