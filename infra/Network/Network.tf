# Create the main VPC.
resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

# Create a public subnet inside the VPC.
# map_public_ip_on_launch=true makes new EC2 instances receive public IPs automatically.
resource "aws_subnet" "subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

# Attach an Internet Gateway to the VPC.
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "main-igw"
  }
}

# Create a public route table for internet access.
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "public-route-table"
  }
}

# Add the default route to the Internet Gateway.
resource "aws_route" "public_internet_access" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Associate the subnet with the public route table.
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Create the security group used by the EC2 instances.
resource "aws_security_group" "allow_traffic" {
  name        = "allow_traffic"
  description = "Allow HTTP and NFS traffic"
  vpc_id      = aws_vpc.vpc.id

  tags = {
    Name = "allow_traffic"
  }
}

# Allow HTTP from anywhere on the internet.
resource "aws_vpc_security_group_ingress_rule" "allow_http_ipv4" {
  security_group_id = aws_security_group.allow_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

# Allow NFS traffic only from inside the VPC.
resource "aws_vpc_security_group_ingress_rule" "allow_nfs_ipv4" {
  security_group_id = aws_security_group.allow_traffic.id
  cidr_ipv4         = aws_vpc.vpc.cidr_block
  from_port         = 2049
  ip_protocol       = "tcp"
  to_port           = 2049
}

# Optional but useful if you want SSH into the instance later.
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ipv4" {
  security_group_id = aws_security_group.allow_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound_ipv4" {
  security_group_id = aws_security_group.allow_traffic.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# Export the subnet ID for other modules.
output "subnet_id" {
  value = aws_subnet.subnet.id
}

# Export the VPC ID for other modules.
output "vpc" {
  value = aws_vpc.vpc.id
}

# Export the security group ID for other modules.
output "allow_traffic" {
  value = aws_security_group.allow_traffic.id
}
