from .configurator_interface import ConfiguratorInterface
import yaml
from api.timeseries_simulator.timeseries.timeseries_simulator import (
    TimeSeriesParams,
)


class YamlConfigurator(ConfiguratorInterface):
    def __init__(self, path: str):
        self.path = path

    def configure(self) -> list[TimeSeriesParams]:
        with open(self.path, "r") as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)
        return self._params(configuration)
