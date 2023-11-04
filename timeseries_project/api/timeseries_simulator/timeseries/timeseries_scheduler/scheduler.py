from jinja2 import Environment, FileSystemLoader
from multiprocessing import Process
import psutil
import os
from api.serializers import SimulatorSerializer
from api.timeseries_simulator.timeseries.timeseries_configurator.configurator_manager import (
    ConfiguratorManager,
)
from api.timeseries_simulator.timeseries.timeseries_producer.producer_creator import (
    ProducerCreator,
)
from api.models import Simulator, Dataset
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesSimulator,
)
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timeseries_project.settings")
django.setup()


class Scheduler:
    # A dictionary to store the mapping of process name to process ID.
    __name_to_pid = {}
    __dag_id = 0

    def __init__(self, simulator_name):
        """
        target (function): The function to be scheduled.
        args: arguments to be passed to the target function.
        """
        self.simulator_name = simulator_name
        self.interval = None

        # Creating a jinja2 template for the DAG file.
        file_dir = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(file_dir))
        self.__template = env.get_template("template_dag.jinja2")

    def start(self, interval=None):
        """
        Starts the execution of the process.
        interval: CRON expression for the interval at which the scheduler should run.
        """
        if not interval:
            # Create a process for the simulator.
            self.process = Process(
                target=Scheduler.run_simulator, args=(self.simulator_name,)
            )

            self.process.start()

            # Store the process ID in the dictionary.
            Scheduler.__name_to_pid[self.process.name] = self.process.pid
            return

        # Store the interval.
        self.interval = interval

        # Generate a DAG file for the airflow task.
        self.__generate_dag()

        # Make the value of the pid as 0, as it's not a process but rather an airflow task.
        Scheduler.__name_to_pid[self.process.name] = 0

    @staticmethod
    def run_simulator(simulator_name):
        """
        Runs the simulator and saves the results to the sink.

        Args:
            simulator_name (str): The name of the simulator to run.

        Note:
            This method is run in a separate process or an airflow task.
        """
        # Get the simulator
        simulator = Simulator.objects.get(name=simulator_name)

        # Get the serializer for the simulator
        serializer = SimulatorSerializer(simulator)

        # Get the dataset IDs associated with the simulator
        datasets = simulator.datasets.values()

        # Get the time series parameters
        time_series_param_list = (
            ConfiguratorManager("django")
            .create_configurator(serializer=serializer)
            .configure()
        )

        for time_series_params, dataset in zip(time_series_param_list, datasets):
            time_series_simulator = TimeSeriesSimulator(time_series_params)
            result_time_series = time_series_simulator.simulate()

            # Send the time series to the sink
            ProducerCreator("kafka").create(
                generator_name=dataset["generator_name"],
                attribute_name=dataset["attribute_name"],
                topic=simulator.sink_name,
                host="localhost",
                port=9092,
            ).produce(result_time_series)

            ProducerCreator("django").create(
                identifier=dataset["id"], model=Dataset
            ).produce(result_time_series)

        simulator.status = "Succeeded"
        simulator.save()

    def __generate_dag(self):
        """
        Generates a DAG file for the airflow task.
        """
        # Create a DAG file for the airflow task.
        dag_file = self.__template.render(
            dag_id=Scheduler.__dag_id,
            interval=self.interval,
            simulator_name=self.simulator_name,
        )

        # Increment the DAG ID.
        Scheduler.__dag_id += 1

        # Create a DAG file for the airflow task.
        with open(
            f"./api/timeseries_simulator/timeseries/timeseries_scheduler/dags/dag_{Scheduler.__dag_id}.py",
            "w",
        ) as file:
            file.write(dag_file)

    def stop(self):
        """
        Terminates the process with the given process ID.
        """
        simulator_pid = Scheduler.__name_to_pid.get(self.simulator_name, None)

        # Check if the process exists.
        if simulator_pid is None:
            return

        # Check if the process is an airflow task.
        if simulator_pid == 0:
            # Delete the DAG file.
            return

        psutil.Process(simulator_pid).terminate()
        del Scheduler.__name_to_pid[self.simulator_name]
