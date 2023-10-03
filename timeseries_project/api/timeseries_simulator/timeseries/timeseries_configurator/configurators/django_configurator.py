from typing import List

from .configurator_interface import ConfiguratorInterface
from rest_framework import serializers
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesParams,
)


class DjangoConfigurator(ConfiguratorInterface):
    def __init__(self, serializer: serializers.ModelSerializer):
        self.serializer = serializer

    def configure(self) -> list[TimeSeriesParams]:
        """Configures the simulator using the Django serializer."""
        return self._params(self.serializer.data)
