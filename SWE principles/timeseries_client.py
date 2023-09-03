import pandas as pd

from timeseries.configuration_manager import ConfigManager
from timeseries.timeseries_producer import TimeSeriesProducer
from timeseries.timeseries_simulator import TimeSeriesGenerator
from timeseries.timeseries_components.generators.seasonality import (
    SeasonalityGenerator,
)
from timeseries.timeseries_components.generators.trend import (
    TrendGenerator,
)
from timeseries.timeseries_components.transformers.noise import (
    NoiseComponent,
)
from timeseries.timeseries_components.transformers.outlier import (
    OutlierComponent,
)


def main():
    # Reading the configuration file
    config_manager = ConfigManager()
    time_series_params = config_manager.params

    # Creating the time series generator
    time_series_generator = TimeSeriesGenerator()

    # Generating the time series
    time_series = time_series_generator.generate()

    # Saving the time series
    time_series_producer = TimeSeriesProducer("./datasets.csv", time_series)
    time_series_producer.to_csv()


if __name__ == "__main__":
    main()
