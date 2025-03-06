FROM apache/airflow
RUN pip install apache-airflow-providers-apache-spark==4.8.1
RUN pip install apache-airflow-providers-common-compat==1.2.2


USER root

RUN apt update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64
RUN export JAVA_HOME

COPY dags /opt/airflow/dags
COPY include /opt/airflow/include