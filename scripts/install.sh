#!/bin/bash

echo "Fetching Airflow from Helm chart ..."
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow

echo "Installing Airflow ..."
helm install airflow-k8 apache-airflow/airflow --namespace airflow --debug

echo "Forwarding port to localhost ..."
kubectl port-forward svc/airflow-k8-webserver 8080:8080 -n airflow
