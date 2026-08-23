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
        print(response)
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


if __name__ == "__main__":
    print("Changing the bucket public access or ownership")
    s3_function = {
        1: add_bucket_public_access,
        2: remove_bucket_public_access,
        3: get_public_access_block,
        4: change_bucket_ownership,
    }
    keys = list(s3_function.keys())
    choice = int(
        input(
            "Please choose a option:\n1: Add Bucket Public Access\n2: Remove Bucket Public Access\n3: Get Public Access Block\n4: Change Bucket Ownership to preferred\n"
        )
    )
    bucket_name = str(input(f"Enter the bucket name:")).strip()
    if choice in keys:
        if choice == 1:
            print(f"Adding the bucket access(public)")
            add_bucket_public_access(bucket_name)
        elif choice == 2:
            print(f"Removing the bucket ownership")
            remove_bucket_public_access(bucket_name)
        elif choice == 3:
            print(f"Getting the public access block")
            get_public_access_block(bucket_name)
        elif choice == 4:
            print(f"Changing the bucket ownership")
            change_bucket_ownership(bucket_name)
    else:
        print(f"Invalid option {choice}")
