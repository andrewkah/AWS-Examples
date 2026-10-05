import boto3
from botocore.exceptions import ClientError
import urllib.parse

class S3Manager:
    def __init__(self, region_name = 'us-east-1'):
        self.region_name = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)

    def list_buckets(self):
        try:
            print('Please wait...')
            response = self.s3_client.list_buckets()
            for bucket in response.get('Buckets', []):
                print(f" - {bucket['Name']}")
        except ClientError as e:
            print(f"Error occurred while listing buckets: {e}")
            return []
    def list_objects(self, bucket_name):
        try:
            print('Please wait...')
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if not any(response.get('Contents', [])):
                print(f"No objects  found in bucket '{bucket_name}'")
                exit()
            print(f"Objects in bucket '{bucket_name}':")
            for obj in response.get('Contents', []):
                print(f" - {obj['Key']}")
        except ClientError as e:
            print(f"Error occurred while listing objects in bucket '{bucket_name}': {e}")
    def download_file(self, bucket_name, object_key, download_path):
        try:
            print('Please wait...')
            response = self.s3_client.download_file(bucket_name, object_key, download_path)
            print(f"Downloaded '{object_key}' from bucket '{bucket_name}' to '{download_path}'")
            return response
        except ClientError as e:
            print(f"Error occurred while downloading file from bucket '{bucket_name}': {e}")
    def upload_file(self, bucket_name, local_path, object_key):
        try:
            print('Please wait...')
            response = self.s3_client.put_object(Body=open(local_path, "rb"), Bucket=bucket_name, Key=object_key)
            print(f"Uploaded '{local_path}' to bucket '{bucket_name}' as '{object_key}'")
            return response
        except ClientError as e:
            print(f"Error occurred while uploading file to bucket '{bucket_name}': {e}")
    
    def get_object_metadata(self, bucket_name, object_key):
        try:
            print('Please wait...')
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            return response
        except ClientError as e:
            print(f"Error occurred while getting metadata for object '{object_key}' in bucket '{bucket_name}': {e}")
            return None
        
    def add_object_prefix(self, bucket_name, object_key, prefix):
        try:
            print('Please wait...')
            response = self.s3_client.copy_object(Bucket=bucket_name, Key=prefix + object_key, CopySource={'Bucket': bucket_name, 'Key': object_key})
            print(f"Added prefix '{prefix}' to object '{object_key}' in bucket '{bucket_name}'")
            return response
        except ClientError as e:
            print(f"Error occurred while adding prefix to object '{object_key}' in bucket '{bucket_name}': {e}")
            
    # CREATING A BUCKET
    def create_bucket(self, bucket_name):
        try:
            print('Please wait...')
            if self.region_name == 'us-east-1':
                response = self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                response = self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region_name})
            print(f"Bucket '{bucket_name}' created in region '{self.region_name}'")
            return response
        except ClientError as e:
            print(f"Error occurred while creating bucket '{bucket_name}': {e}")
            return None
    def change_storage_class(self, bucket_name, object_key, target_class):
        try:
            print("Please wait...")
            response = self.s3_client.copy_object(Bucket=bucket_name, Key=object_key, CopySource={'Bucket': bucket_name, 'Key': object_key}, StorageClass=target_class, MetadataDirective='COPY')
            print(f"Bucekt '{bucket_name}' is now of storage type '{target_class}'")
            return response
        except ClientError as e:
            print(f"Error occurred while changing storage class: {e}")
    
    # DELETING A BUCKET
    def delete_bucket(self, bucket_name):
        try:
            print('Please wait...')
            response = self.s3_client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted successfully.")
            return response
        except ClientError as e:
            print(f"Error occurred while deleting bucket '{bucket_name}': {e}")
            return None
        
    def delete_bucket_objects(self, bucket_name):
        try:
            print('Please wait...')
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                for obje in response['Contents']:
                    self.s3_client.delete_object(Bucket=bucket_name, Key=obje['Key'])
                    print(f"Deleted object '{obje['Key']}' from bucket '{bucket_name}'")
            else:
                print(f"No contents found in the bucket '{bucket_name}'.")
            return response
        except ClientError as e:
            print(f"Error occurred while deleting objects from bucket '{bucket_name}': {e}")
            return None
    
    # UPDATING OBJECT METADATA
    def update_object_metadata(self, bucket_name, object_key, metadata):
        try:
            print('Please wait...')
            # Copy the object to itself with new metadata
            copy_source = {'Bucket': bucket_name, 'Key': object_key}
            self.s3_client.copy_object(Bucket=bucket_name, Key=object_key, CopySource=copy_source, Metadata=metadata, MetadataDirective='REPLACE')
            print(f"Metadata for object '{object_key}' in bucket '{bucket_name}' updated successfully.")
        except ClientError as e:
            print(f"Error occurred while updating metadata for object '{object_key}' in bucket '{bucket_name}': {e}")
    
    # DELETING AN OBJECT
    def delete_object(self, bucket_name, object_key):
        try:
            print('Please wait...')
            response = self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            print(f"Object '{object_key}' deleted from bucket '{bucket_name}'")
            return response
        except ClientError as e:
            print(f"Error occurred while deleting object '{object_key}' from bucket '{bucket_name}': {e}")
            return None
    # Object Locking
    def enable_object_locking(self, bucket_name):
        try:
            print('Please wait...')
            response = self.s3_client.put_object_lock_configuration(Bucket=bucket_name, ObjectLockConfiguration={'ObjectLockEnabled': 'Enabled'})
            print(f"Object locking enabled for bucket '{bucket_name}'")
            return response
        except ClientError as e:
            print(f"Error occurred while enabling object locking for bucket '{bucket_name}': {e}")
            return None
if __name__ == "__main__":
    s3_manager = S3Manager()
    s3_functions = {
        1: s3_manager.list_buckets,
        2: s3_manager.list_objects,
        3: s3_manager.create_bucket,
        4: s3_manager.delete_bucket,
        5: s3_manager.delete_bucket_objects,
        6: s3_manager.upload_file,
        7: s3_manager.update_object_metadata,
        8: s3_manager.add_object_prefix
    }
    keys = list(s3_functions.keys())
    # introduce this script and ask for the bucket name
    print(f"Welcome to the S3 Manager script, where you can create, view and delete buckets and their objects.\nPlease choose the operation you intend to carry out!")
    print(f"1: List buckets\n2: List objects in a bucket\n3: Create a bucket\n4: Delete a bucket\n5: Delete objects from a bucket\n6: Upload a file\n7: Update object metadata\n8: Add prefix to an object")
    choice = int(input("Enter the number corresponding to your choice: "))
    if choice in keys:
        if choice in [2, 3, 4, 5, 6, 7, 8]:
            # ask for the bucket name
            bucket_name = input("Enter the bucket name: ")
            if choice in [2, 4, 5]:
                # check if the bucket exists
                buckets = s3_manager.list_buckets()
                if not any(bucket['Name'] == bucket_name for bucket in buckets['Buckets']):
                    print(f"Bucket '{bucket_name}' does not exist. Please create it first.")
                    exit()
                s3_functions[choice](bucket_name)
            elif choice == 3:
                s3_functions[choice](bucket_name)
            elif choice == 6:
                object_key = input("Enter the object key: ")
                local_path = input("Enter your current file/file-path to upload: ")
                s3_functions[choice](bucket_name, local_path, object_key)
            elif choice == 7:
                object_key = input("Enter the object key: ")
                metadata_input = input("Enter metadata as key1=value1,key2=value2,...: ")
                metadata = dict(item.split("=") for item in metadata_input.split(","))
                s3_functions[choice](bucket_name, object_key, metadata)
            elif choice == 8:
                object_key = input("Enter the object key: ")
                prefix = input("Enter the prefix to add: ")
                s3_functions[choice](bucket_name, object_key, prefix)
        else:
            print("Buckets in your account:")
            response = s3_functions[choice]()
    else:
        print("Invalid choice. Please try again.")        