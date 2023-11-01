import threading
from typing import override
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SimulatorSerializer
from .models import Simulator, Dataset
from .timeseries_simulator.timeseries.timeseries_configurator.configurator_manager import (
    ConfiguratorManager,
)
from .timeseries_simulator.timeseries.timeseries_producer.producer_creator import (
    ProducerCreator,
)
from .timeseries_simulator.timeseries.timeseries_simulator import TimeSeriesSimulator


class AddView(APIView):
    @override
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
    @override
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

        # Start a new thread to run the simulator, and associate it with the name of the simulator
        simulator_thread = threading.Thread(
            target=StartView.run_simulator, args=(request, serializer)
        )

        # Update the status of the simulator to "Running"
        simulator = Simulator.objects.get(name=request.data["name"])
        simulator.status = "Running"
        simulator.save()

        # Start the simulator thread
        simulator_thread.start()

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

            if simulator.stop_flag:  # If the stop flag is True, stop the simulator
                return

            # Send the time series to the sink
            ProducerCreator("kafka").create(
                generator_name=dataset["generator_name"],
                attribute_name=dataset["attribute_name"],
                topic=simulator.sink_name,
                host="localhost",
                port=9092,
            ).produce(result_time_series)

        simulator.status = "Succeeded"
        simulator.stop_flag = False
        simulator.save()


class ListView(APIView):
    @override
    def get(self, request) -> Response:
        """
        Returns the values of all the simulators in the database.

        Returns:
            Response: HTTP response containing simulator data (200 OK).
        """
        simulator_values = SimulatorSerializer(Simulator.objects.all(), many=True).data
        return Response(data=simulator_values, status=status.HTTP_200_OK)


class RestartView(APIView):
    @override
    def post(self, request) -> Response:
        """
        Restarts the simulator thread, by starting a new thread and setting the stop flag to False.

        Args:
            request: The HTTP request object containing the name of the simulator to restart.

        Returns:
            Response: HTTP response indicating success (200 OK).
        """
        simulator = Simulator.objects.get(name=request.data["name"])
        simulator.status = "Running"

        serializer = SimulatorSerializer(simulator)

        simulator.stop_flag = False  # Set the stop flag to False
        simulator.save()

        # Start a new thread for the simulator
        simulator_thread = threading.Thread(
            target=StartView.run_simulator, args=(request, serializer)
        )

        # Start the simulator thread
        simulator_thread.start()

        return Response(status=status.HTTP_200_OK)


class StopView(APIView):
    @override
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
        simulator.status = "Failed"
        simulator.stop_flag = True
        simulator.save()

        return Response(status=status.HTTP_200_OK)


class StatusView(APIView):
    @override
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
