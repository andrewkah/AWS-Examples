package aws.examples.s3manager;

import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3AsyncClient;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.DeleteBucketRequest;
import software.amazon.awssdk.services.s3.model.DeleteObjectRequest;
import software.amazon.awssdk.services.s3.model.HeadBucketRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;
import software.amazon.awssdk.services.s3.model.S3Exception;

public class CrudOperations {
    public String regionName;
    public final S3AsyncClient s3Client;
    public CrudOperations(String regionName){
        s3Client = DependencyFactory.s3Client();
        this.regionName = regionName;
    }

    // Create methods: Create Bucket, Upload file(s)
    public void createNewBucket(S3AsyncClient s3Client, String bucketName){
        try{
            s3Client.createBucket(CreateBucketRequest.builder().bucket(bucketName).build());
            System.out.println("Creating Bucket: "+ bucketName);
            s3Client.waiter().waitUntilBucketExists(HeadBucketRequest.builder().bucket(bucketName).build());
            System.out.println(bucketName + " is ready.");
            System.out.println("%n");
        } catch(S3Exception e){
            System.err.println(e.awsErrorDetails().errorMessage());
            System.exit(1);
        }
    }

    public static void uploadNewFile(S3AsyncClient s3Client, String bucketName, String key, String localPath){
        try{
            System.out.println("Uploading your file to: "+ bucketName);
            PutObjectRequest request = PutObjectRequest.builder().bucket(bucketName).key(key).contentType('text/plain').build();
            PutObjectResponse response = s3Client.putObject(request, RequestBody.fromFile(localPath));
            System.out.println("File uploaded successfully. ETag: "+ response.eTag());
        } catch(S3Exception e){
            System.err.println(e.awsErrorDetails().errorMessage());
            System.exit(1);
        }
    }

    // Read methods: List Buckets, list objects, download object(s)

    // Update methods: Update object meatadata

    // Delete methods: Delete bucket, Delete object(s)
}
