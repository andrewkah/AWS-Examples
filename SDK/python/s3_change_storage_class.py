import s3_manager

if __name__ == "__main__":
    """Change the storage class of the selected bucket
    """
    s3_storage_classes = {
        1: 'STANDARD',
        2: 'STANDARD_IA',
        3: 'ONEZONE_IA',
        4: 'INTELLIGENT_TIER',
        5: 'GLACIER',
        6: 'DEEP_ARCHIEVE',
        7: 'GLACIER_IR',
    }
    keys =  list(s3_storage_classes.keys())
    print('Welcome, please choose the bucket whose storage is to be changed.')
    s3 = s3_manager.S3Manager()
    s3.list_buckets()
    bucket_name = str(input(f"Enter the bucket name:")).strip()
    print("\n--- Objects found in bucket ---")
    response = s3.s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        print(f" -> '{obj['Key']}'")
    print("-------------------------------\n")
    object_key = str(input(f"Enter your object key:")).strip()
    storage_class = int(input("Storage Classes\n1: STANDARD\n2: STANDARD_IA\n3: ONEZONE_IA\n4: INTELLIGENT_TIER\n5: GLACIER\n6: DEEP_ARCHIEVE\n7: GLACIER_IR\nChoose the target storage class:"))
    print(f"Changing storage class for {bucket_name}")
    if storage_class in keys:
        s3.change_storage_class(bucket_name, object_key, s3_storage_classes[storage_class])
    else:
        print('Invalid choice, please try again.')