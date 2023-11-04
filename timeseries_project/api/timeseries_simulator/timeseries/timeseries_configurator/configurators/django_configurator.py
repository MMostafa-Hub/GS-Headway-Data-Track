

from typing import List
from .configurator_interface import ConfiguratorInterface
from rest_framework import serializers
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesParams,
)


class DjangoConfigurator(ConfiguratorInterface):
    def __init__(self, serializer: serializers.ModelSerializer):
        """
        Initializes a DjangoConfigurator instance.

        Args:
            serializer (serializers.ModelSerializer): The Django serializer containing configuration data.
        """
        self.serializer = serializer


    def configure(self) -> List[TimeSeriesParams]:
        """
        Configures the simulator using the Django serializer.

        Returns:
            list[TimeSeriesParams]: A list of TimeSeriesParams objects based on the configuration data.
        """
        return self._params(self.serializer.data)
