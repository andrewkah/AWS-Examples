import s3_manager
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3", region_name="us-east-1")


def remove_bucket_public_access(bucket_name):
    try:
        print("Please wait...")
        response = s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            },
        )
        print("Bucket Policies have been restricted")
        print(response)
        return response
    except ClientError as e:
        print(f"Failed to complete: {e}")


def add_bucket_public_access(bucket_name):
    try:
        print("Please wait...")
        response = s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        print(response)
        return response
    except ClientError as e:
        print(f"Failed to complete: {e}")


def get_public_access_block(bucket_name):
    try:
        print("Please wait...")
        response = s3.get_public_access_block(Bucket=bucket_name)
        print(response["PublicAccessBlockConfiguration"])
        return response
    except ClientError as e:
        print(f"Failed to complete: {e}")


def change_bucket_ownership(bucket_name):
    try:
        print("Please wait...")
        response = s3.put_bucket_ownership_controls(
            Bucket=bucket_name,
            OwnershipControls={"Rules": [{"ObjectOwnership": "BucketOwnerPreferred"}]},
        )
        print(response)
        return response
    except ClientError as e:
        print(f"Failed to change bucket ownership: {e}")

def apply_bucket_policy(bucket_name, file_path):
    try:
        print('Please wait...')
        with open(file_path, 'r') as f:
            policy_template = f.read()
        final_policy = policy_template.replace('<BUCKET_NAME>', bucket_name)
        response = s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=final_policy
        )
        print(response["Policy"])
        return response
    except ClientError as e:
        print(f"Failed to apply bucket policy: {e}")

def get_bucket_policies(bucket_name):
    try:
        print('Please wait...')
        response = s3.get_bucket_policy(Bucket=bucket_name)
        print(response["Policy"])
        return response
    except ClientError as e:
        print(f"Failed to get bucket policy: {e}")

if __name__ == "__main__":
    print("Changing the bucket public access or ownership")
    s3_function = {
        1: add_bucket_public_access,
        2: remove_bucket_public_access,
        3: get_public_access_block,
        4: change_bucket_ownership,
        5: get_bucket_policies,
        6: apply_bucket_policy,
    }
    keys = list(s3_function.keys())
    choice = int(
        input(
            "Please choose a option:\n1: Add Bucket Public Access\n2: Remove Bucket Public Access\n3: Get Public Access Block\n4: Change Bucket Ownership to preferred\n5: Get Bucket Policy\n6: Apply Bucket Policy\n"
        )
    )
    bucket_name = str(input(f"Enter the bucket name:")).strip()
    if choice in keys:
        if choice in [1, 2, 3, 4, 5]:
            s3_function[choice](bucket_name)
        elif choice == 6:
            file_path = str(input(f"Enter the file path:")).strip()
            s3_function[choice](bucket_name, file_path)
    else:
        print(f"Invalid option {choice}")
