from .transformer import Transformer
import pandas as pd
import numpy as np


class OutlierTransformer(Transformer):
    def __init__(self, outlier_ratio: float) -> None:
        self.outlier_ratio = outlier_ratio

    def transform(self, time_series: pd.Series) -> pd.Series:
        """
        Add random outliers to the time series data.

        Args:
            time_series (pd.Series): The input time series data to which outliers will be added.

        Returns:
            pd.Series: A pandas Series representing the time series data with added random outliers.

        This method introduces random outliers to the provided time series data by selecting a
        specified percentage of data points and replacing them with random outlier values
        within the range [-1, 1].

        Args:
        - time_series: The input time series data to which random outliers will be added.

        Returns:
        - pd.Series: A pandas Series containing the original time series data with random
          outliers introduced.
        """

        # Calculate the number of outliers to add based on the outlier ratio
        num_outliers = int(time_series.shape[0] * self.outlier_ratio)

        # If there are no outliers to add, return the original time series
        if num_outliers == 0:
            return time_series

        # Choose random indices for the outliers without replacement
        outlier_indices = np.random.choice(
            time_series.shape[0], num_outliers, replace=False
        )

        # Create a copy of the time series data to modify
        data_with_outliers = time_series.copy()

        # Generate random outlier values between -1 and 1
        outliers = np.random.uniform(-1, 1, num_outliers)

        # Add the outliers to the time series data
        data_with_outliers[outlier_indices] = outliers

        return data_with_outliers
