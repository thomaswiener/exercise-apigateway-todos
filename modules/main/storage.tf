# tfsec:ignore:aws-iam-no-policy-wildcards
# tfsec:ignore:aws-s3-enable-versioning
# tfsec:ignore:aws-s3-enable-bucket-logging
# tfsec:ignore:aws-s3-encryption-customer-key
# tfsec:ignore:aws-s3-enable-bucket-encryption
resource "aws_s3_bucket" "storage" {
  bucket = local.bucket_storage
}

resource "aws_s3_bucket_acl" "storage" {
  bucket = aws_s3_bucket.storage.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "storage" {
  bucket                  = aws_s3_bucket.storage.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}