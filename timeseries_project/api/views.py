import threading
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UseCaseSerializer
from .models import UseCase, Dataset
from .timeseries_simulator.timeseries.timeseries_configurator.configurator_manager import (
    ConfiguratorManager,
)
from .timeseries_simulator.timeseries.timeseries_producer.producer_creator import (
    ProducerCreator,
)
from .timeseries_simulator.timeseries.timeseries_simulator import TimeSeriesSimulator


class AddView(APIView):
    def post(self, request):
        """Adds a use case to the database, and starts a new thread to run the simulator."""
        serializer = UseCaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()  # Save the use case to the database

        # Start a new thread to run the simulator, and associate it with the name of the use case
        simulator_thread = threading.Thread(
            target=AddView.run_simulator, args=(request, serializer)
        )

        # Update the status of the use case to "Running"
        use_case = UseCase.objects.get(name=request.data["name"])
        use_case.status = "Running"
        use_case.save()

        # Start the simulator thread
        simulator_thread.start()

        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def run_simulator(request, serializer):
        """Runs the simulator and saves the results to the database."""
        dataset_ids = UseCase.objects.get(
            name=request.data["name"]
        ).datasets.values_list(
            "id", flat=True
        )  # Get the dataset IDs associated with the use case
        use_case = UseCase.objects.get(name=request.data["name"])  # Get the use case

        # Get the time series parameters from the database
        time_series_param_list = (
            ConfiguratorManager("django")
            .create_configurator(serializer=serializer)
            .configure()
        )
        for time_series_params, dataset_id in zip(time_series_param_list, dataset_ids):
            time_series_simulator = TimeSeriesSimulator(time_series_params)
            result_time_series = time_series_simulator.simulate()

            # Check the use case again to see if it has been stopped by stop_simulator view
            use_case = UseCase.objects.get(
                name=request.data["name"]
            )  # Get the use case

            if use_case.flag:  # If the stop flag is True, stop the simulator
                return

            # Save the time series to the database
            ProducerCreator("django").create(
                identifier=dataset_id, model=Dataset
            ).produce(result_time_series)

        use_case.status = "Succeeded"
        use_case.flag = False
        use_case.save()


class StartView(APIView):
    def post(self, request):
        pass


class ListView(APIView):
    def get(self, request):
        """Returns the values of the use cases"""
        use_cases_simulator_values = UseCaseSerializer(
            UseCase.objects.all(), many=True
        ).data
        return Response(data=use_cases_simulator_values, status=status.HTTP_200_OK)


class RestartView(APIView):
    def post(self, request):
        """Restarts the simulator thread, by starting a new thread and setting the stop flag to False."""
        request_data_simulator_name = request.data["name"]
        use_case = UseCase.objects.get(name=request_data_simulator_name)
        use_case.status = "Running"

        serializer = UseCaseSerializer(use_case)
        # Start a new thread for the simulator
        simulator_thread = threading.Thread(
            target=AddView.run_simulator, args=(request, serializer)
        )
        use_case.flag = False  # Set the stop flag to False
        use_case.save()

        # Start the simulator thread
        simulator_thread.start()

        return Response(status=status.HTTP_200_OK)


class StopView(APIView):
    def post(self, request):
        """Stops the simulator thread, by setting the stop flag to True."""
        request_data_simulator_name = request.data["name"]

        # Check if there's a simulator with this name
        try:
            use_case = UseCase.objects.get(name=request_data_simulator_name)
        except:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the simulator is running
        if use_case.status != "Running":
            return Response(
                data="The simulator has finished", status=status.HTTP_400_BAD_REQUEST
            )

        # Stop the simulator
        use_case.status = "Failed"
        use_case.flag = True
        use_case.save()

        return Response(status=status.HTTP_200_OK)


class StateView(APIView):
    def get(self, request):
        """Checks the status of the simulator."""
        request_data_simulator_name = request.query_params.get("name")

        # Check if there's a simulator with this name
        try:
            use_case = UseCase.objects.get(name=request_data_simulator_name)
        except:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data=use_case.status, status=status.HTTP_200_OK)
