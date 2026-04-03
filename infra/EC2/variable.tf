# Subnet where the EC2 instance will be launched.
variable "subnet_id" {
  type = string
}

# Security group attached to the EC2 instance.
variable "security_group_id" {
  type = string
}

# Friendly instance name used in EC2 tags.
variable "instance_name" {
  type = string
}

# Server mode:
# - "docker" => Docker + Nginx container
variable "server_mode" {
  type = string
}

