from .transformer import Transformer
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, override


class NormalizationTransformer(Transformer):
    def __init__(self, feature_range: Tuple[int, int]) -> None:
        super().__init__()
        self.feature_range = feature_range


    def transform(self, time_series: pd.Series) -> pd.Series:
        """
        Normalize the time series data to a specified feature range.

        Args:
            time_series (pd.Series): The input time series data to be normalized.

        Returns:
            pd.Series: A pandas Series representing the normalized time series data.

        This method normalizes the provided time series data by subtracting the mean and dividing
        by the standard deviation. It uses the MinMaxScaler from scikit-learn to perform the
        normalization, mapping the data to the specified 'feature_range'.

        Args:
        - time_series: The input time series data to be normalized.

        Returns:
        - pd.Series: A pandas Series containing the normalized time series data within the
          specified 'feature_range'.
        """

        scaler = MinMaxScaler(feature_range=self.feature_range)
        values = time_series.values
        values = np.array(values).reshape(-1, 1)
        return pd.Series(scaler.fit_transform(values))
