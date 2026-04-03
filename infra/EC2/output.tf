# Public IP of this EC2 instance.
output "public_ip" {
  value = aws_instance.web.public_ip
}

# Instance ID of this EC2 instance.
output "instance_id" {
  value = aws_instance.web.id
}
