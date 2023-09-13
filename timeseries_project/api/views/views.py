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


SIMULATOR_THREADS_ID = {}


def run_simulator(request, serializer):
    dataset_ids = UseCase.objects.get(name=request.data["name"]).datasets.values_list(
        "id", flat=True
    )
    time_series_param_list = ConfigurationManager.sqlite_db(serializer)
    for time_series_params, dataset_id in zip(time_series_param_list, dataset_ids):
        time_series_simulator = TimeSeriesSimulator(time_series_params)
        result_time_series = time_series_simulator.simulate()
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
    simulator_thread.start()

    # Save the thread ID in the SIMULATOR_THREADS_ID dictionary
    SIMULATOR_THREADS_ID[request.data["name"]] = simulator_thread.ident

    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_simulators(request: Request) -> Response:
    """Returns the names of the simulators that are available."""
    use_cases_simulator_names = UseCase.objects.values_list("name", flat=True)
    return Response(data=use_cases_simulator_names, status=status.HTTP_200_OK)


@api_view(["POST"])
def restart_simulator(request: Request) -> Response:
    request_data_simulator_name = request.data["name"]
    use_case = UseCase.objects.get(name=request_data_simulator_name)
    use_case.status = "Running"

    # Start a new thread for the simulator
    simulator_thread = threading.Thread(target=run_simulator, args=(request, use_case))
    simulator_thread.start()

    # Save the thread ID in the SIMULATOR_THREADS_ID dictionary
    SIMULATOR_THREADS_ID[request_data_simulator_name] = simulator_thread.ident

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def stop_simulator(request: Request) -> Response:
    request_data_simulator_name = request.data["name"]
    use_case = UseCase.objects.get(name=request_data_simulator_name)
    use_case.status = "Failed"

    # Get the thread ID from the SIMULATOR_THREADS_ID dictionary
    thread_id = SIMULATOR_THREADS_ID.get(request_data_simulator_name)

    if thread_id:
        # Use the thread ID to stop the simulator
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                thread.join(timeout=1)
                break

    return Response(status=status.HTTP_200_OK)
