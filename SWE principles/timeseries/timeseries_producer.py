import pandas as pd


class TimeSeriesProducer:
    """This class is responsible for writing the time series to any format."""

    @staticmethod
    def csv(path: str, time_series: pd.Series):
        """Writes the time series to a CSV file."""
        time_series.to_csv(path, index=False)
