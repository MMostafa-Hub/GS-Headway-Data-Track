
from .transformer import Transformer
import numpy as np
import pandas as pd


class MissingValueTransformer(Transformer):
    def __init__(self, missing_values_ratio: float) -> None:
        super().__init__()
        self.missing_values_ratio = missing_values_ratio
        self.missing_indices: np.ndarray = np.array([])


    def transform(self, time_series: pd.Series) -> pd.Series:
        """
        Add missing values to the time series data within a specified date range.

        Args:
            time_series (pd.Series): The input time series data to which missing values
                will be added.

        Returns:
            pd.Series: A pandas Series representing the time series data with added
                missing values.

        This method introduces missing values to the provided time series data by randomly
        selecting a specified percentage of data points and setting them to NaN. The number
        of missing values is determined by 'missing_values_ratio', which should be a float
        between 0 and 1.

        Args:
        - time_series: The input time series data to which missing values will be added.

        Returns:
        - pd.Series: A pandas Series with the same data as the input time series, but with
          missing values (NaN) introduced at random positions.
        """
        num_missing = int(time_series.shape[0] * self.missing_values_ratio)
        self.missing_indices = np.random.choice(
            time_series.shape[0], size=num_missing, replace=False
        )

        data_with_missing = time_series.copy()
        data_with_missing[self.missing_indices] = np.nan

        return data_with_missing
