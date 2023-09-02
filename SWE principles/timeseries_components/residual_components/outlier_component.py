from residual_component import ResidualComponent
import pandas as pd
import numpy as np


class OutlierComponent(ResidualComponent):
    def __init__(self, outlier_ratio: float) -> None:
        self.outlier_ratio = outlier_ratio

        # These attributes maybe used in the future
        self.anomaly_mask: np.ndarray
        self.outlier_indices: np.ndarray

    def transform(self, time_series: pd.Series) -> pd.Series:
        """Add outliers to the time series data."""
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

        # Create a boolean mask to indicate the positions of the added outliers
        self.anomaly_mask = np.zeros(time_series.shape[0], dtype=bool)
        self.anomaly_mask[outlier_indices] = True

        return data_with_outliers
