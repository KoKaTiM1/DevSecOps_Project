// Terraform variables for EKS cluster
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "devsecops-cluster"
}

variable "region" {
  description = "AWS region to create resources in"
  type        = string
  default     = "us-east-1"
}

variable "node_count" {
  description = "Number of nodes in the managed node group"
  type        = number
  default     = 1
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
  default     = "t3.small"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC (if creating a new VPC)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_id" {
  description = "ID of an existing VPC to deploy the cluster into (optional)"
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "List of subnet IDs to use for the EKS cluster"
  type        = list(string)
  default     = []
}

variable "public_subnets" {
  description = "List of public subnet IDs to use (optional - pass to reuse existing VPC)"
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "List of private subnet IDs to use (optional - pass to reuse existing VPC)"
  type        = list(string)
  default     = []
}

variable "enable_irsa" {
  description = "Whether to enable IAM Roles for Service Accounts (IRSA) via OIDC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to created resources"
  type        = map(string)
  default     = {}
}
