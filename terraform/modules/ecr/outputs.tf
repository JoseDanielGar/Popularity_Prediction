output "repository_arn" {
  value       = aws_ecr_repository.ecr.arn # nombre, tipo y atributo del recurso
  description = "Repository ARN."
}
