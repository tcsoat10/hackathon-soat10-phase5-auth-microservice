variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "hacka-soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "db_password" {
  description = "Database user password"
  type        = string
}

variable "db_name" {
  default = "auth_microservice_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "secret_key" {
  description = "Database username"
  type        = string
}

variable "aws_account_id" {}
variable "auth_api_key" {}

variable "application_image" {
  description = "Docker image for the application"
  type        = string
  default     = ""
}

locals {
  application_image = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/soattc-auth-app:latest"
}