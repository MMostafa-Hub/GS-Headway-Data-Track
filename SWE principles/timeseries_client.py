from timeseries.configuration_manager import ConfigurationManager
from timeseries.timeseries_producer import TimeSeriesProducer
from timeseries.timeseries_simulator import TimeSeriesSimulator


def main():
    # Reading the configuration file
    time_series_params = ConfigurationManager.yaml("./config.yaml")

    # Creating the time series generator
    time_series_generator = TimeSeriesSimulator(time_series_params)

    # Generating the time series
    time_series = time_series_generator.simulate()

    # Saving the time series
    TimeSeriesProducer.csv("./timeseries.csv", time_series)


if __name__ == "__main__":
    main()
