resource "aws_s3_bucket" "aws-examples-andrew-terraform" {
    # bucket = "aws-examples-andrew-terraform"

    tags = {
        Name  = "My First terraform Bucket"
        Environment = "Learning"
    }
}