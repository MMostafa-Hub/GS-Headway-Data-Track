from main_component import MainComponent
import pandas as pd
import numpy as np


class StaticSignalComponent(MainComponent):
    def __init__(self, time_index: pd.DatetimeIndex, magnitude: float) -> None:
        """Initialize the magnitude of the static signal component."""
        super().__init__(time_index)
        self.magnitude = magnitude

    @property
    def values(self) -> pd.Series:
        """Add static signal component to a time series."""
        return pd.Series(
            np.ones(self.time_index.shape[0]) * self.magnitude, index=self.time_index
        )
