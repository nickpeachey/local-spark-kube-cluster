from airflow.decorators import task, dag
from pendulum import datetime


@dag(
    start_date=datetime(2024,6,4),
    schedule=None,
    catchup=False
)
def test_run():

    @task
    def run():
        pass
    
    run()

test_run()
