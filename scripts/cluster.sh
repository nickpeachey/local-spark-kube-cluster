#!/bin/bash

echo "Creating kubernetes cluster and check it ..."

kind create cluster --name airflow-cluster --config ./kind-cluster.yaml

echo "Cluster info"
kubectl cluster-info

echo "Nodes info"
kubectl get nodes -o wide
