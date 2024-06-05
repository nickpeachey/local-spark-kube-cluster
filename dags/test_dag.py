from airflow.decorators import task, dag
from pendulum import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


@dag(
    start_date=datetime(2024,6,4),
    schedule=None,
    catchup=False
)
def test_dag():

    @task
    def run_spark():
        spark = SparkSession.builder.appName("demo").getOrCreate()

        df = spark.createDataFrame(
            [
                ("sue", 32),
                ("li", 3),
                ("bob", 75),
                ("heo", 13),
            ],
            ["first_name", "age"],
        )

        df1 = df.withColumn(
            "life_stage",
            when(col("age") < 13, "child")
            .when(col("age").between(13, 19), "teenager")
            .otherwise("adult"),
        )

        df1.show()
    
    run_spark()

test_dag()
