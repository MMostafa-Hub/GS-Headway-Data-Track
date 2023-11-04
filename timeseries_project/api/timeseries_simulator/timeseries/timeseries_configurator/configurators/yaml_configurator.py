from typing import List
from .configurator_interface import ConfiguratorInterface
import yaml
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesParams,
)


class YamlConfigurator(ConfiguratorInterface):
    def __init__(self, path: str):
        """
        Initializes a YamlConfigurator instance.

        Args:
            path (str): The path to the YAML configuration file.
        """
        self.path = path

    def configure(self) -> List[TimeSeriesParams]:
        """
        Configures the simulator using a YAML configuration file.

        Returns:
            list[TimeSeriesParams]: A list of TimeSeriesParams objects based on the configuration in the YAML file.
        """
        with open(self.path, "r") as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)
        return self._params(configuration)
