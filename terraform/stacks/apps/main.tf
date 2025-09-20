module "project_ecr_repository" {
  source           = "../../modules/ecr"
  keep_tags_number = var.keep_tags_number
  repository_name  = var.repository_name
}


module "project_eks_cluster" {
  source = "../../modules/eks"

  cluster_name                   = var.cluster_name
  k8s_cluster_version            = var.k8s_cluster_version
  cluster_endpoint_public_access = var.cluster_endpoint_public_access
}
