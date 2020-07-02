resource "aws_s3_bucket" "mybucket" {
  bucket_prefix = "my-codebuild-bucket"
  acl           = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "AES256"
      }
    }
  }
}