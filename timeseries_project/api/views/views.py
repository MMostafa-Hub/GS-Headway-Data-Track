import threading
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import UseCaseSerializer
from ..models import UseCase, Dataset
from .timeseries_simulator.timeseries.configuration_manager import ConfigurationManager
from .timeseries_simulator.timeseries.timeseries_producer import TimeSeriesProducer
from .timeseries_simulator.timeseries.timeseries_simulator import TimeSeriesSimulator

# This dictionary is used to stop the simulator thread
SIMULATOR_THREAD_STOP_FLAG = {}


def run_simulator(request, serializer):
    """Runs the simulator and saves the results to the database."""
    dataset_ids = UseCase.objects.get(name=request.data["name"]).datasets.values_list(
        "id", flat=True
    )  # Get the dataset IDs associated with the use case

    # Get the time series parameters from the database
    time_series_param_list = ConfigurationManager.sqlite_db(serializer)
    for time_series_params, dataset_id in zip(time_series_param_list, dataset_ids):
        time_series_simulator = TimeSeriesSimulator(time_series_params)
        result_time_series = time_series_simulator.simulate()

        # Check if the simulator thread should be stopped
        if SIMULATOR_THREAD_STOP_FLAG[request.data["name"]]:
            return

        # Save the time series to the database
        TimeSeriesProducer.to_django_model(Dataset, dataset_id, result_time_series)


@api_view(["POST"])
def add_use_case(request: Request) -> Response:
    """Adds a use case to the database, and starts a new thread to run the simulator."""
    serializer = UseCaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()  # Save the use case to the database

    # Start a new thread to run the simulator, and associate it with the name of the use case
    simulator_thread = threading.Thread(
        target=run_simulator, args=(request, serializer)
    )

    # Create a stop flag for the simulator thread
    SIMULATOR_THREAD_STOP_FLAG[request.data["name"]] = False

    # Update the status of the use case to "Running"
    use_case = UseCase.objects.get(name=request.data["name"])
    use_case.status = "Running"
    use_case.save()

    # Start the simulator thread
    simulator_thread.start()

    simulator_thread.join()  # Wait for the simulator thread to finish

    # Update the status of the use case to "Succeeded"
    use_case.status = "Succeeded"
    use_case.save()

    # Update the stop flag of the simulator thread
    SIMULATOR_THREAD_STOP_FLAG[request.data["name"]] = True

    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_simulators(request: Request) -> Response:
    """Returns the names of the simulators that are available."""
    use_cases_simulator_names = UseCase.objects.values_list("name", flat=True)
    return Response(data=use_cases_simulator_names, status=status.HTTP_200_OK)


@api_view(["POST"])
def restart_simulator(request: Request) -> Response:
    """Restarts the simulator thread, by starting a new thread and setting the stop flag to False."""
    request_data_simulator_name = request.data["name"]
    use_case = UseCase.objects.get(name=request_data_simulator_name)
    use_case.status = "Running"

    # Start a new thread for the simulator
    simulator_thread = threading.Thread(target=run_simulator, args=(request, use_case))
    simulator_thread.start()

    # Create a stop flag for the simulator thread
    SIMULATOR_THREAD_STOP_FLAG[request.data["name"]] = False

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def stop_simulator(request: Request) -> Response:
    """Stops the simulator thread, by setting the stop flag to True."""
    request_data_simulator_name = request.data["name"]
    use_case = UseCase.objects.get(name=request_data_simulator_name)
    use_case.status = "Failed"

    # Stop the simulator thread
    SIMULATOR_THREAD_STOP_FLAG[request_data_simulator_name] = True

    return Response(status=status.HTTP_200_OK)
