from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import (
    SeasonalityComponentSerializer,
    DatasetSerializer,
    UseCaseSerializer,
)


@api_view(["POST"])
def add_seasonality_component(request: Request) -> Response:
    serializer = SeasonalityComponentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def add_dataset(request: Request) -> Response:
    serializer = DatasetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def add_use_case(request: Request) -> Response:
    serializer = UseCaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
