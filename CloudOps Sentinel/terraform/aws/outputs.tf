output "ecr_repository_url" {
  description = "Docker repository for the API image."
  value       = aws_ecr_repository.api.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "aws_account_id" {
  description = "Current AWS account ID."
  value       = data.aws_caller_identity.current.account_id
}

