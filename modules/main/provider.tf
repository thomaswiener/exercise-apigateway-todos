terraform {
  required_version = ">=1.1.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.31.0"
    }
  }
  backend "s3" {
  }
}

provider "aws" {
  region = data.aws_caller_identity.current.account_id
  default_tags {
    tags = {
      env = var.env
    }
  }
}
