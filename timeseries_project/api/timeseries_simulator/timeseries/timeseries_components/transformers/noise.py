from typing import override
from .transformer import Transformer
import pandas as pd
import numpy as np


class NoiseTransformer(Transformer):
    def __init__(self, noise_level: float) -> None:
        super().__init__()
        self.noise_level = noise_level

    @override
    def transform(self, time_series: pd.Series) -> pd.Series:
        """
        Add random noise to the time series data.

        Args:
            time_series (pd.Series): The input time series data to which noise will be added.

        Returns:
            pd.Series: A pandas Series representing the time series data with added random noise.

        This method introduces random noise to the provided time series data by generating
        normally distributed random values with a specified standard deviation (noise_level).
        These random values are added to the original data, resulting in a noisy time series.

        Args:
        - time_series: The input time series data to which random noise will be added.

        Returns:
        - pd.Series: A pandas Series with the same data as the input time series, but with
          added random noise.
        """

        noise = np.random.normal(0, self.noise_level, size=len(time_series))
        return pd.Series(time_series.copy() + noise)
