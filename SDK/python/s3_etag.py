import hashlib
import s3_manager

def calculate_s3_etag(data):
    """ Calculate the Etag value for a bucket object.
    Md5 works for small objects
    """
    crc_value = 0
    with open(data, 'rb') as f:
        md5 = hashlib.md5(f.read())
        crc_value = md5.hexdigest()
    return crc_value

if __name__ == "__main__":
    """ Validating the Etag of an object uploaded to the bucket
    """
    s3client = s3_manager.S3Manager()
    # Get the bucket name
    bucket_name = input("Enter the bucket name: ")
    # Get the object key
    object_key = input("Enter the object key: ")
    # Get the file name
    file_name = input("Enter the file name: ")
    # Upload the file to the bucket
    print("Uploading the file to the bucket...")
    s3client.upload_file(bucket_name, file_name, object_key)
    checksum = calculate_s3_etag(file_name)
    print("Calculated etag value: ",checksum)
    # Get the checksum value from the bucket
    print("Getting the etag value from the bucket...")
    contents = s3client.get_object_metadata(bucket_name, object_key)
    print("Etag value from the bucket: ", contents['ETag'])
    