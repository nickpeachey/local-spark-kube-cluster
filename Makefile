CLUSTER_NAME := "airflow-cluster"
SERVICE_NAME := "airflow"
HELM_NAME := "airflow-k8"
HELM_REPO := "apache-airflow/airflow"
IMAGE_NAME := "airflow-base"
TAG := "1.0.0"

init:
	@echo "Installing Kubectl, KinD, Helm, docker and docker compose ..."
	@brew install kubectl
	@brew install kind
	@brew install helm
	@brew install docker
	@brew install docker-compose

cluster:
	@echo "Creating kubernetes cluster and check it ..."
	@kind create cluster --name ${CLUSTER_NAME} --config kind-cluster.yaml
	@kubectl cluster-info
	@kubectl get nodes -o wide

ns:
	@kubectl create namespace ${SERVICE_NAME}
	@kubectl get namespaces

fetch:
	@echo "Fetching airflow from Helm chart"
	@helm repo add apache-airflow https://airflow.apache.org
	@helm repo update
	@helm search repo airflow

install:
	@echo "Installing airflow ..."
	@helm install ${HELM_NAME} ${HELM_REPO} --namespace ${SERVICE_NAME} --debug

upgrade:
	@echo "Upgrading airflow ..."
	@helm upgrade --install ${HELM_NAME} ${HELM_REPO} --namespace ${SERVICE_NAME} -f values.yaml --debug

forward:
	@echo "Forwarding port to local ..."
	@kubectl port-forward svc/airflow-k8-webserver 8080:8080 -n ${SERVICE_NAME}

clean:
	@echo "Cleaning up installation ..."
	@helm uninstall ${HELM_NAME}

load:
	@echo "Building airflow image ..."
	@docker build -t ${IMAGE_NAME}:${TAG} .
	@kind load docker-image ${IMAGE_NAME}:${TAG} --name ${CLUSTER_NAME}
