# login to AWS ECR
dklogin:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# build and tag docker image
dkbuild:
	docker build --rm --no-cache --platform linux/amd64 -t ${APP_NAME}:${APP_VERSION} --label version=${APP_VERSION} -f ${DIR}/Dockerfile ${DIR}
	docker tag ${APP_NAME}:${APP_VERSION} ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/${APP_NAME}:${APP_VERSION}

# push docker image to AWS ECR
dkpush:dklogin dkbuild
	-AWS_PAGER="" aws ecr create-repository --repository-name ${APP_NAME} --region us-east-1
	docker push ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/${APP_NAME}:${APP_VERSION}

# terraform initialize
init:
	terraform -chdir=$(shell pwd)/terraform/stacks/${STACK} init -backend-config=$(shell pwd)/terraform/environments/${ENV}/${STACK}/backend.tfvars

# terraform plan and create a plan file
plan:init
	terraform -chdir=$(shell pwd)/terraform/stacks/${STACK} plan -var-file=$(shell pwd)/terraform/environments/${ENV}/${STACK}/terraform.tfvars -out=.tfplan

# apply the created plan file
apply:plan
	terraform -chdir=$(shell pwd)/terraform/stacks/${STACK} apply .tfplan

# terraform destroy all resources
destroy:
	terraform -chdir=$(shell pwd)/terraform/stacks/${STACK} destroy -var-file=$(shell pwd)/terraform/environments/${ENV}/${STACK}/terraform.tfvars

# configure kubectl to use the EKS cluster
eksconfig:
	-AWS_PAGER="" aws sts get-caller-identity
	aws eks update-kubeconfig --region us-east-1 --name ${CLUSTER_NAME}


# apply k8s manifests to the EKS cluster
#eksapply: eksconfig eksingress
eksapply:
	envsubst < "$(shell pwd)/k8s/dashboard-app-deployment.yaml" | kubectl apply -f -
	envsubst < "$(shell pwd)/k8s/song-popularity-api-deployment.yaml" | kubectl apply -f -
	kubectl apply -f $(shell pwd)/k8s/ingress.yaml

# delete all k8s resources from the EKS cluster
eksdestroy:
	kubectl delete -f $(shell pwd)/k8s/ingress.yaml
	envsubst < "$(shell pwd)/k8s/dashboard-app-deployment.yaml" | kubectl delete -f -
	envsubst < "$(shell pwd)/k8s/song-popularity-api-deployment.yaml" | kubectl delete -f -

# install nginx ingress controller on EKS
eksingress:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
	helm repo update
	-helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=LoadBalancer

# delete nginx ingress controller from EKS
eksdeleteingress:
	kubectl -n ingress-nginx delete svc ingress-nginx-controller
	kubectl delete ns ingress-nginx
	-helm uninstall ingress-nginx -n ingress-nginx

# watch for the external url of the ingress controller
eksingressurl:
	kubectl get svc -n ingress-nginx ingress-nginx-controller -w
