// Terraform outputs for EKS cluster
output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.cluster.name
}

output "cluster_endpoint" {
  description = "EKS cluster API endpoint"
  value       = aws_eks_cluster.cluster.endpoint
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate authority data for the cluster"
  value       = aws_eks_cluster.cluster.certificate_authority[0].data
}

output "kubeconfig_command" {
  description = "Command to configure kubectl for this cluster"
  value       = "aws eks --region ${var.region} update-kubeconfig --name ${aws_eks_cluster.cluster.name}"
}

output "node_group_name" {
  description = "Managed node group name"
  value       = aws_eks_node_group.node_group.node_group_name
}

output "node_group_arn" {
  description = "ARN of the managed node group"
  value       = aws_eks_node_group.node_group.arn
}

output "node_instance_types" {
  description = "Instance types for the node group"
  value       = aws_eks_node_group.node_group.instance_types
}

output "node_desired_capacity" {
  description = "Desired size for the managed node group"
  value       = aws_eks_node_group.node_group.scaling_config[0].desired_size
}
