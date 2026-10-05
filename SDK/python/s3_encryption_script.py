import boto3
import os
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from s3_encryption import S3EncryptionClient, S3EncryptionClientConfig
from s3_encryption.materials.kms_keyring import KmsKeyring

kms = boto3.client("kms", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
script_dir = Path(__file__).resolve().parent.parent.parent
env_path = script_dir / ".env"
load_dotenv(dotenv_path=env_path)

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
def create_s3_encryption_client():
    try:
        # get the existing kms_key arm for the Customer Managed Key
        print("Creating encryption client...")
        key_id = os.environ["AWS_ALIAS_S3_MANAGED_KEY"]
        kms_key_arn = kms.list_aliases(KeyId=key_id)["Aliases"][0]["AliasArn"]
        # create the keyring
        keyring = KmsKeyring(kms, kms_key_arn)
        # create the s3 client
        s3_client = S3EncryptionClient(s3, S3EncryptionClientConfig(keyring=keyring))
        return s3_client
    except ClientError as e:
        print(f"Error occurred while creating encryption client: {e}")
        return None

if __name__ == "__main__":
    """S3 Encryption with KMS or Client Encryption

    Raises:
        e: Select the encryption method you want to use: KMS or Client Encryption
    """
    encryption_options = {
        1: "KMS",
        2: "Client Encryption",
        3: "Enable Object Encryption",
        4: "Enable Object Encryption with SSE-C",
        5: "Exit",
    }
    print("Select the encryption method you want to use:")
    for key, value in encryption_options.items():
        print(f"{key}. {value}")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("Creating an bucket with KMS enabled encryption!")
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
    elif choice == 2:
        print("Creating an bucket with Client Encryption!")
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
        s3_client = create_s3_encryption_client()
        object_key = str(input(f"Enter your object key:")).strip()
        file_path = str(input(f"Enter the file path:")).strip()
        response = s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
        if "ETag" in response:
            print(f"Object '{object_key}' uploaded successfully.")
        else:
            print(f"Object '{object_key}' upload failed.")
    elif choice == 3:
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
            print(f"Object '{object_key}' upload failed.")
    elif choice == 4:
        print("Creating an bucket with SSE-C enabled encryption and adding an object!")
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
        print('Adding SSE-C Bucket Encryption to the bucket')
        put_bucket_encryption_SSE_C(bucket_name)
        object_key = str(input(f"Enter your object key:")).strip()
        file_path = str(input(f"Enter the file path:")).strip()
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
        if "ETag" in response:
            print(f"Object '{object_key}' uploaded successfully.")
        else:
            print(f"Object '{object_key}' upload failed.")
    elif choice == 5:
        exit()
    else:
        print("Invalid choice. Please try again.")
    # print("Creating an bucket with KMS enabled encryption and adding an object!")
    # bucket_name = str(input("Enter your bucket name:")).strip()
    # try:
    #     s3.head_bucket(Bucket=bucket_name)
    #     print(f"Bucket '{bucket_name}' already exists.")
    # except ClientError as e:
    #     error_code = e.response['Error']['Code']        
    #     if error_code == '404':
    #         print(f"Bucket '{bucket_name}' not found. Auto-creating it now...")
    #         s3.create_bucket(Bucket=bucket_name)
    #         print(f"Bucket '{bucket_name}' successfully created.")
    #     else:
    #         # If it's a 403 Forbidden or another error, raise it
    #         raise e
    # print('Adding KMS Bucket Encryption to the bucket')
    # put_bucket_encryption_KMS(bucket_name)
    # object_key = str(input(f"Enter your object key:")).strip()
    # file_path = str(input(f"Enter the file path:")).strip()
    # response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
    # if "ETag" in response:
    #     print(f"Object '{object_key}' uploaded successfully.")
    # else:
    #     print(f"Failed to upload object '{object_key}'.")
        