resource "aws_s3_bucket" "aws-examples-andrew-terraform" {
    # bucket = "aws-examples-andrew-terraform"

    tags = {
        Name  = "My First terraform Bucket"
        Environment = "Learning"
    }
}

resource "aws_s3_object" "object-1" {
    bucket = aws_s3_bucket.aws-examples-andrew-terraform.id
    key = "object-1.txt"
    source = "object-1.txt"
    etag = filemd5("object-1.txt")
} 