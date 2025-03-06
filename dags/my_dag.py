# my_dag.py
from airflow.decorators import dag, task
from datetime import datetime

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pandas as pd
    
@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)
def my_dag():
    @task.pyspark(conn_id="spark_default")
    def read_data(spark: SparkSession, sc: SparkContext) -> pd.DataFrame:
        df = spark.read.csv("./include/data.csv", header="true")

        df.show()

        df.createOrReplaceTempView("products")
        products = spark.sql("SELECT * FROM products where product = 'Keyboard'")

        products.show()

        for row in products:
            print(row.product)

        return df.toPandas()
    
    read_data()

my_dag()