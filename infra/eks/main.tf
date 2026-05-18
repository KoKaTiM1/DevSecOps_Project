// Minimal EKS cluster and managed node group using existing VPC/subnets
data "aws_caller_identity" "current" {}

resource "aws_eks_cluster" "cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = length(var.subnet_ids) > 0 ? var.subnet_ids : [var.vpc_id]
    endpoint_private_access = false
    endpoint_public_access  = true
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy]
}

resource "aws_eks_node_group" "node_group" {
  cluster_name    = aws_eks_cluster.cluster.name
  node_group_name = "${var.cluster_name}-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = length(var.subnet_ids) > 0 ? var.subnet_ids : [var.vpc_id]

  scaling_config {
    desired_size = var.node_count
    max_size     = var.node_count
    min_size     = 1
  }

  instance_types = [var.node_instance_type]

  remote_access {
    # optional, disabled by default. Provide key_name if you want SSH access.
    ec2_ssh_key = ""
  }

  depends_on = [aws_eks_cluster.cluster]
}
