from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SimulatorSerializer
from .models import Simulator
from .timeseries_simulator.timeseries.timeseries_configurator.configurator_manager import (
    ConfiguratorManager,
)
from .timeseries_simulator.timeseries.timeseries_producer.producer_creator import (
    ProducerCreator,
)
from .timeseries_simulator.timeseries.timeseries_simulator import TimeSeriesSimulator
from multiprocessing import Process
import psutil


class AddView(APIView):
    def post(self, request) -> Response:
        """
        Adds a new simulator to the database.

        Args:
            request: The HTTP request object containing data for the new simulator.

        Returns:
            Response: HTTP response indicating success (201 Created) or failure (400 Bad Request).
        """
        serializer = SimulatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()  # Save the simulator to the database

        return Response(status=status.HTTP_201_CREATED)


class StartView(APIView):
    def post(self, request) -> Response:
        """
        Starts the simulator thread.

        Args:
            request: The HTTP request object containing the name of the simulator to start.

        Returns:
            Response: HTTP response indicating success (200 OK) or failure (400 Bad Request).
        """
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
            serializer = SimulatorSerializer(simulator)
        except Exception:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        # Start a new process to run the simulator, and associate it with the name of the simulator
        simulator_process = Process(
            target=StartView.run_simulator, args=(request, serializer)
        )

        # Start the simulator process
        simulator_process.start()

        # Update the status of the simulator to "Running"
        simulator = Simulator.objects.get(name=request.data["name"])
        simulator.process_id = simulator_process.pid
        simulator.status = "Running"
        simulator.save()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def run_simulator(request, serializer):
        """
        Runs the simulator and saves the results to the database.

        Args:
            request: The HTTP request object containing the name of the simulator.
            serializer: The serializer for the simulator.

        Note:
            This method is run in a separate thread.
        """
        # Get the dataset IDs associated with the simulator
        datasets = Simulator.objects.get(name=request.data["name"]).datasets.values()

        # Get the simulator
        simulator = Simulator.objects.get(name=request.data["name"])

        # Get the time series parameters from the database
        time_series_param_list = (
            ConfiguratorManager("django")
            .create_configurator(serializer=serializer)
            .configure()
        )
        for time_series_params, dataset in zip(time_series_param_list, datasets):
            time_series_simulator = TimeSeriesSimulator(time_series_params)
            result_time_series = time_series_simulator.simulate()

            # Check the simulator again to see if it has been stopped by StopView
            simulator = Simulator.objects.get(name=request.data["name"])

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


class ListView(APIView):
    def get(self, request) -> Response:
        """
        Returns the values of all the simulators in the database.

        Returns:
            Response: HTTP response containing simulator data (200 OK).
        """
        simulator_values = SimulatorSerializer(Simulator.objects.all(), many=True).data
        return Response(data=simulator_values, status=status.HTTP_200_OK)


class RestartView(APIView):
    def post(self, request) -> Response:
        """
        Restarts the simulator thread, by starting a new thread and setting the stop flag to False.

        Args:
            request: The HTTP request object containing the name of the simulator to restart.

        Returns:
            Response: HTTP response indicating success (200 OK).
        """
        simulator = Simulator.objects.get(name=request.data["name"])

        # Update the status of the simulator to "Running"
        simulator.status = "Running"

        # Get the serializer for the simulator
        serializer = SimulatorSerializer(simulator)

        # Start a new process for the simulator
        simulator_process = Process(
            target=StartView.run_simulator, args=(request, serializer)
        )

        # Start the simulator process
        simulator_process.start()

        # Update the process ID of the simulator
        simulator.process_id = simulator_process.pid

        # save the new status and process ID
        simulator.save()

        return Response(status=status.HTTP_200_OK)


class StopView(APIView):
    def post(self, request) -> Response:
        """
        Stops the simulator thread, by setting the stop flag to True.

        Args:
            request: The HTTP request object containing the name of the simulator to stop.

        Returns:
            Response: HTTP response indicating success (200 OK) or failure (400 Bad Request).
        """
        # Check if there's a simulator with this name
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
        except Exception:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the simulator is running
        if simulator.status != "Running":
            return Response(
                data="The simulator has finished", status=status.HTTP_400_BAD_REQUEST
            )

        # Stop the simulator
        psutil.Process(simulator.process_id).terminate()
        simulator.status = "Failed"
        simulator.save()

        return Response(status=status.HTTP_200_OK)


class StatusView(APIView):
    def get(self, request) -> Response:
        """
        Checks the status of the simulator.

        Args:
            request: The HTTP request object containing the name of the simulator.

        Returns:
            Response: HTTP response containing the status of the simulator (200 OK).
        """
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
        except Exception:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data=simulator.status, status=status.HTTP_200_OK)
