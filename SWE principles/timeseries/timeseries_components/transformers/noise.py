from .transformer import Transformer
import pandas as pd
import numpy as np


class NoiseTransformer(Transformer):
    def __init__(self, noise_level: float) -> None:
        super().__init__()
        self.noise_level = noise_level

    def transform(self, time_series: pd.Series) -> pd.Series:
        """Add noise to the time series data."""
        noise = np.zeros_like(time_series)
        for i in range(time_series.shape[0]):
            noise[i] = (
                np.random.normal(0, abs(time_series[i]) * self.noise_level)
                if self.noise_level > 0
                else 0
            )
        return pd.Series(time_series + noise)
