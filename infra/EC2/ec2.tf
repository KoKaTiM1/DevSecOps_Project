# Find the most recent Amazon Linux 2023 AMI in the selected region.
data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Create one EC2 instance of type t3.micro.
resource "aws_instance" "web" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.micro"
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
  associate_public_ip_address = true

  # Render the startup script from a template file.
  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    server_mode        = var.server_mode
  })

  tags = {
    Name = var.instance_name
  }
}