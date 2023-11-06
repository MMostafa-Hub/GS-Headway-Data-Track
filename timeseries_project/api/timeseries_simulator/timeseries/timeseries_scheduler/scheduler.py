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
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesSimulator,
)
import django

# Set the Django settings module for airflow
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timeseries_project.settings")
django.setup()


class Scheduler:
    # A dictionary to store the mapping of process name to process ID.
    __name_to_pid = {}

    def __init__(self, simulator_name):
        """
        simulator_name: The name of the simulator to run.
        """
        self.simulator_name = simulator_name

    def start(self, interval=None):
        """
        Starts the execution of the process.
        """
        # Create a process for the simulator.
        process = Process(target=Scheduler.run_simulator, args=(self.simulator_name,))

        # Start the process.
        process.start()

        # Store the process ID in the dictionary.
        Scheduler.__name_to_pid[self.simulator_name] = process.pid
        print(Scheduler.__name_to_pid)

    @staticmethod
    def run_simulator(simulator_name):
        """
        Runs the simulator and saves the results to the sink.

        Args:
            simulator_name (str): The name of the simulator to run.

        Note:
            This method is run in a separate process or an airflow task.
        """
        from api.models import Simulator

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

        simulator.status = "Succeeded"
        simulator.save()

    def stop(self):
        """
        Terminates the process with the given process ID.
        """
        simulator_pid = Scheduler.__name_to_pid.get(self.simulator_name, None)

        # Check if the process exists.
        if not simulator_pid:
            raise Exception(f"No process with name: {self.simulator_name} exists.")

        try:
            process = psutil.Process(simulator_pid)
            process.terminate()  # terminate the process

        except psutil.NoSuchProcess:
            print(f"No process with PID {simulator_pid} exists.")
        except psutil.AccessDenied:
            print(f"Access denied when trying to terminate process {simulator_pid}.")

        # Delete
        del Scheduler.__name_to_pid[self.simulator_name]
