import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3", region_name="us-east-1")


def put_bucket_encryption_KMS(bucket_name):
    """Create a bucket with AWS KMS encryption, with auto generated key

    Args:
        bucket_name (str): Name of the bucket to create

    Returns:
        JsonResponse: Returns the API response for this task
    """
    try:
        print("Please wait...")
        response = s3.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"},
                        "BucketKeyEnabled": True,
                    }
                ]
            },
        )
        print(response)
        return response
    except ClientError as e:
        print(f"Error occurred while creating bucket '{bucket_name}': {e}")
        return None


def enable_object_encryption(
    bucket_name, object_key, object_body, server_side_encryption="AES256"
):
    print("Please wait...")
    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=object_body,
        ServerSideEncryption=server_side_encryption,
    )
    print(response)
    return response

def put_bucket_encryption_SSE_C(bucket_name, object_key, object_body, server_side_encryption="AES256"):
    try:
        print("Please wait...")
        response = s3.put_object(
            Bucket=bucket_name,
            Key= object_key,
            Body=object_body,
            SSECustomerAlgorithm="AES256",
            SSECustomerKey=os.urandom(32),
        )
        print(response)
        return response
    except ClientError as e:
        print(f"Error occurred while creating bucket '{bucket_name}': {e}")
        return None


if __name__ == "__main__":
    print("Creating an bucket with KMS enabled encryption and adding an object!")
    bucket_name = str(input("Enter your bucket name:")).strip()
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']        
        if error_code == '404':
            print(f"Bucket '{bucket_name}' not found. Auto-creating it now...")
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' successfully created.")
        else:
            # If it's a 403 Forbidden or another error, raise it
            raise e
    print('Adding KMS Bucket Encryption to the bucket')
    put_bucket_encryption_KMS(bucket_name)
    object_key = str(input(f"Enter your object key:")).strip()
    file_path = str(input(f"Enter the file path:")).strip()
    response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
    if "ETag" in response:
        print(f"Object '{object_key}' uploaded successfully.")
    else:
        print(f"Failed to upload object '{object_key}'.")
        