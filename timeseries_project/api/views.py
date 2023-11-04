from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .timeseries_simulator.timeseries.timeseries_scheduler.scheduler import Scheduler
from .serializers import SimulatorSerializer
from .models import Simulator


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
        except Exception:
            return Response(
                data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
            )

        # Start a new process for the simulator
        Scheduler(simulator.name).start(simulator.interval)

        # Update the status of the simulator to "Running"
        simulator.status = "Running"
        simulator.save()

        return Response(status=status.HTTP_200_OK)


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

        # Start a new process for the simulator
        Scheduler(simulator.name).start(simulator.interval)

        # Update the status of the simulator to "Running"
        simulator.status = "Running"
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
        Scheduler(simulator.name).stop()
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
