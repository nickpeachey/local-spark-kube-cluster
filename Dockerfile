FROM apache/airflow:2.8.3
RUN pip install apache-airflow-providers-apache-spark==4.8.1
COPY --chown=airflow:root dags/ /opt/airflow/dags
