import boto3
from botocore import ClientError

s3 = boto3.client('s3', region_name='us_east_1')

def configure_static_webhosting(bucket_name, config_file):
    try:
        print("Please wait...")
        with open(config_file, 'r') as f:
            final_path = f.read()
        response = s3.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=final_path)
        print(response)
    except ClientError as e:
        print(f"Failed to complete: {e}")