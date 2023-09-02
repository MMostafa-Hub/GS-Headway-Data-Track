from main_component import MainComponent
import pandas as pd
import numpy as np


class TrendComponent(MainComponent):
    def __init__(self, magnitude: float, negative: bool = False) -> None:
        """Initialize the magnitude and direction of the trend component.

        Args:
            magnitude (float): the magnitude of the trend component
            negative (bool, optional): Defaulting the trend to be positive.
        """
        super().__init__()
        self.magnitude = magnitude
        self.direction = -1 if negative else 1

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Create trend component for a time series."""
        self.time_index = time_index
        # Getting the time period of the time series in days
        time_period = (self.time_index[-1] - self.time_index[0]).days

        # This implementation I'm not sure about. I think it's not correct.
        # But it's in the legacy code, so I'm keeping it for now.
        trend_component = pd.Series(
            np.linspace(0, time_period / 30 * self.direction, self.time_index.shape[0])
            if self.direction == 1
            else np.linspace(-1 * time_period / 30, 0, self.time_index.shape[0])
        )
        return trend_component * self.magnitude
