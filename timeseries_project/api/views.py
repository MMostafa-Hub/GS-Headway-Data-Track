import threading
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
    def post(self, request):
        """Adds a new simulator to the database"""
        serializer = SimulatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()  # Save the simulator to the database

        return Response(status=status.HTTP_201_CREATED)


class StartView(APIView):
    def post(self, request):
        """Starts the simulator thread."""
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
            serializer = SimulatorSerializer(simulator)
        except Exception as e:
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
        """Runs the simulator and saves the results to the database."""
        # Get the dataset IDs associated with the simulator
        dataset_ids = Simulator.objects.get(
            name=request.data["name"]
        ).datasets.values_list("id", flat=True)

        # Get the simulator
        simulator = Simulator.objects.get(name=request.data["name"])

        # Get the time series parameters from the database
        time_series_param_list = (
            ConfiguratorManager("django")
            .create_configurator(serializer=serializer)
            .configure()
        )
        for time_series_params, dataset_id in zip(time_series_param_list, dataset_ids):
            time_series_simulator = TimeSeriesSimulator(time_series_params)
            result_time_series = time_series_simulator.simulate()

            # Check the simulator again to see if it has been stopped by StopView
            simulator = Simulator.objects.get(name=request.data["name"])

            if simulator.stop_flag:  # If the stop flag is True, stop the simulator
                return

            # Save the time series to the database
            ProducerCreator("django").create(
                identifier=dataset_id, model=Dataset
            ).produce(result_time_series)

        simulator.status = "Succeeded"
        simulator.stop_flag = False
        simulator.save()


class ListView(APIView):
    def get(self, request):
        """Returns the values of the use cases"""
        simulator_values = SimulatorSerializer(Simulator.objects.all(), many=True).data
        return Response(data=simulator_values, status=status.HTTP_200_OK)


class RestartView(APIView):
    def post(self, request):
        """Restarts the simulator thread, by starting a new thread and setting the stop flag to False."""
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
    def post(self, request):
        """Stops the simulator thread, by setting the stop flag to True."""
        # Check if there's a simulator with this name
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
        except:
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
    def get(self, request):
        """Checks the status of the simulator."""
        try:
            simulator = Simulator.objects.get(name=request.data["name"])
        except:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data=simulator.status, status=status.HTTP_200_OK)
