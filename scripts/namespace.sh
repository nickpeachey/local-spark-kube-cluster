#!/bin/bash

echo "Creating kubernetes namespace Airflow ..."

kubectl create namespace airflow
kubectl get namespaces
