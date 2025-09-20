resource "aws_ecr_repository" "ecr" {
  name                 = var.repository_name # usamos la variable de entrada
  image_tag_mutability = "MUTABLE"           # for development purposes
  force_delete         = true
  image_scanning_configuration {
    # Enabling scanning increase the cost
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "lifecycle_policy" {
  repository = aws_ecr_repository.ecr.name # esto genera una dependencia con el recurso anterior
  policy     = local.policy_document       # usamos la variable local
}
