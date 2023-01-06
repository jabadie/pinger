terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 4.48.0"
      }
    }

  backend "s3" {
      bucket = "jabadie-terraform-state"
      key = "state"
      region = "us-west-2"
  }
}