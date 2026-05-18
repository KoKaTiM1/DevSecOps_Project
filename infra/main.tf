terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
  backend "s3" {
    bucket         = "project-final-devopssec-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "project-terraform-locks"
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

module "eks" {
  source = "./eks"
  cluster_name       = "devsecops-cluster"
  region             = "us-east-1"
  vpc_id             = module.vpc.vpc
  subnet_ids         = [module.vpc.subnet_id]
  node_count         = 1
  node_instance_type = "t3.small"
  tags               = {}
}
