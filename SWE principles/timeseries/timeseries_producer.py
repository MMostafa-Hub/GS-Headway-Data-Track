import pandas as pd


class TimeSeriesProducer:
    def __init__(self, path: str, time_series: pd.Series) -> None:
        self.path = path
        self.time_series = time_series

    def to_csv(self):
        """Writes the time series to a CSV file."""
        self.time_series.to_csv(self.path, index=False)
