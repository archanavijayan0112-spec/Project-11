variable "aws_region" {
  type        = string
  description = "AWS region for CloudOps Sentinel."
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Name used for AWS resource naming."
  default     = "cloudops-sentinel"
}

variable "container_port" {
  type        = number
  description = "API container port."
  default     = 8000
}

