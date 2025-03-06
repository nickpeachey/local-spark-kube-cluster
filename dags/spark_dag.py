from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from kubernetes.client import models as k8s

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='spark_job_dag',
    default_args=default_args,
    description='Run Spark job on Kubernetes',
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    
    SPARK_JOB_NAME = "spark-processing-job"
    NAMESPACE = "spark-jobs"
    KUBERNETES_CONN_ID = "kubernetes_default"
    SPARK_IMAGE = "gcr.io/spark-operator/spark:v3.3.2"
    
    spark_task = SparkKubernetesOperator(
        task_id='run_spark_job',
        namespace=NAMESPACE,
        kubernetes_conn_id=KUBERNETES_CONN_ID,
        application_file="""
        apiVersion: sparkoperator.k8s.io/v1beta2
        kind: SparkApplication
        metadata:
          name: {{ task.task_id }}
        spec:
          type: Java
          mode: cluster
          image: {}
          imagePullPolicy: Always
          mainClass: com.example.YourMainClass
          mainApplicationFile: "local:///opt/spark/examples/jars/your-jar-file.jar"
          sparkVersion: "3.3.2"
          hadoopConf:
            fs.defaultFS: "file:///"
          volumes:
            - name: spark-local-dir
              hostPath:
                path: /tmp
          driver:
            cores: 1
            coreLimit: "1000m"
            memory: "512m"
            labels:
              version: "3.3.2"
            serviceAccount: spark
            volumeMounts:
              - name: spark-local-dir
                mountPath: "/tmp"
          executor:
            cores: 1
            instances: 1
            memory: "512m"
            labels:
              version: "3.3.2"
            volumeMounts:
              - name: spark-local-dir
                mountPath: "/tmp"
          restartPolicy:
            type: Never
        """.format(SPARK_IMAGE),
        do_xcom_push=True,
        dag=dag
    )