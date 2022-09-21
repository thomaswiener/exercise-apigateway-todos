provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      env = "dev"
    }
  }
}

module "main" {
  source = "../../modules/main"

  env = "dev"
}