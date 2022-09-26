provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      env = "dev"
    }
  }
}

#terraform {
#  backend "s3" {
#    region         = "eu-central-1"
#    bucket         = "terraform-state-643355622722"
#    key            = "terraform-dev.tfstate"
#    encrypt        = true
#    dynamodb_table = "terraform-state-lock"
#  }
#}

module "main" {
  source = "../../modules/main"

  env = "dev"
}