terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
  backend "s3" {
    bucket         = "eyedar-prod-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "eyedar-prod-terraform-locks"
  }
}

provider "aws" {
  region = "us-east-1"
}


module "vpc" {
  source = "./Network"
}

module "ec2" {
  source = "./EC2"

  subnet_id          = module.vpc.subnet_id
  security_group_id  = module.vpc.allow_traffic
  instance_name      = "web-server"
  server_mode        = "docker"
  
}
