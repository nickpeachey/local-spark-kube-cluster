#!/bin/bash

echo "Installing Kubectl, KinD, Helm, docker and docker compose ..."

brew install kubectl
brew install kind
brew install helm
brew install docker
brew install docker-compose

echo "It's ready, you can proceed to install Airflow"
