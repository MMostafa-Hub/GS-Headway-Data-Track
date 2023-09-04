from typing import Any

import pandas as pd
import yaml
from .timeseries_simulator import TimeSeriesParams
from .timeseries_components.generators.seasonality import SeasonalityGenerator
from .timeseries_components.generators.trend import TrendGenerator
from .timeseries_components.transformers.noise import NoiseTransformer
from .timeseries_components.transformers.outlier import OutlierTransformer


class ConfigurationManager:
    @staticmethod
    def _params(config: dict[str, Any]) -> TimeSeriesParams:
        """Unpacks the configuration dictionary and returns the time series parameters."""
        # Time index parameters
        time_index_config = config["time_index"]
        start_date = pd.Timestamp(time_index_config["start_date"])
        end_date = pd.Timestamp(time_index_config["end_date"])
        # T stands for minutes
        frequency = f'{time_index_config["sampling_frequency_in_minutes"]}' + "T"

        time_index = pd.date_range(start=start_date, end=end_date, freq=frequency)

        # Main components parameters
        multiplicative = config["multiplicative"]

        # Trend component parameters
        main_components_config = config["main_components"]
        trend_coefficients = main_components_config["trend"]["coefficients"]

        # Seasonality component parameters
        seasonality_params_config_list = main_components_config["seasonality"]

        main_components = [TrendGenerator(trend_coefficients)] + [
            SeasonalityGenerator(**seasonality_params_config)
            for seasonality_params_config in seasonality_params_config_list
        ]

        # Residual components parameters
        residual_components_config = config["residual_components"]
        noise_params_config = residual_components_config["noise"]
        outlier_params_config = residual_components_config["outliers"]

        residual_components = [
            NoiseTransformer(**noise_params_config),
            OutlierTransformer(**outlier_params_config),
        ]

        # Creating the time series parameters
        time_series_params = TimeSeriesParams(
            time_index=time_index,
            main_components=main_components,
            residual_components=residual_components,
            multiplicative=multiplicative,
        )

        return time_series_params

    @staticmethod
    def yaml(path: str) -> TimeSeriesParams:
        with open(path, "r") as file:
            config_data = file.read()

        config = yaml.load(config_data, Loader=yaml.FullLoader)
        return ConfigurationManager._params(config)
