from residual_component import ResidualComponent
import numpy as np
import pandas as pd


class MissingValueComponent(ResidualComponent):
    def __init__(self, missing_values_ratio: float) -> None:
        super().__init__()
        self.missing_values_ratio = missing_values_ratio
        self.missing_values_indices: np.ndarray

    def transform(self, time_series: pd.Series) -> pd.Series:
        """Add missing values to the time series data within a specified date range."""
        num_missing = int(time_series.shape[0] * self.missing_values_ratio)
        self.missing_indices = np.random.choice(
            time_series.shape[0], size=num_missing, replace=False
        )

        data_with_missing = time_series.copy()
        data_with_missing[self.missing_indices] = np.nan

        return data_with_missing
