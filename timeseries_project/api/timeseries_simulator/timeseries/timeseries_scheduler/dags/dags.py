from airflow import DAG
from airflow.decorators import task
import os
import django

# Add the path to the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timeseries_project.settings")
django.setup()

from api.models import Simulator

simulators = Simulator.objects.all()
for simulator in simulators:
    if simulator.interval:
        with DAG(
            dag_id=simulator.name,
            schedule_interval=simulator.interval,
            start_date=simulator.start_date,
            is_paused_upon_creation=False,
        ) as dag:
            from api.timeseries_simulator.timeseries.timeseries_scheduler.scheduler import (
                Scheduler,
            )

            @task
            def run_simulation():
                Scheduler.run_simulator(
                    simulator_name=simulator.name,
                )

            run_simulation()
    