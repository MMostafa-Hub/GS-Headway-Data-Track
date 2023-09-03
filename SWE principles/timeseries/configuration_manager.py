import pandas as pd
import yaml
from typing import Any
from timeseries_simulator import TimeSeriesParams


class ConfigManager:
    def __init__(self, path: str = "config.yaml", config_type: str = "yaml") -> None:
        """Initialize the configuration manager."""
        self.path = path
        self.config_type = config_type
        self.time_series_params: TimeSeriesParams

    def __read_yaml_config(self) -> TimeSeriesParams:
        """
        This function returns the yaml configuration file as a TimeSeriesParams object.
        """
        with open(self.path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        start_date = pd.Timestamp(config["start_date"])
        end_date = pd.Timestamp(config["end_date"])
        frequency = config["sampling_frequency_in_minutes"] + "T"
        multiplicative = config["multiplicative"]

    @property
    def params(self) -> TimeSeriesParams:
        if self.config_type == "yaml":
            self.time_series_params = self.__read_yaml_config()
        return self.time_series_params
