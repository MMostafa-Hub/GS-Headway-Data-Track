from .generator import Generator
import pandas as pd
import numpy as np


class SeasonalityGenerator(Generator):
    def __init__(self, period: int, amplitude: int = 1, in_days: bool = True) -> None:
        """Initialize the period of the seasonality component.
        Args:
            period (int): the period of the seasonality component
            amplitude (int): the amplitude of the seasonality component
            in_days (bool): if True, the period is in days, otherwise in hours
        """
        super().__init__()
        self.period = period
        self.amplitude = amplitude
        self.in_days = in_days

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Generates a sinusoidal seasonality component for a time series."""
        # sequence of numbers from 0 to the number of timestamps
        time = np.arange(len(time_index))

        return pd.Series(
            self.amplitude * np.sin(2 * np.pi * time / self.__total_period)
        )

    @property
    def __total_period(self) -> int:
        """Convert the total period to minutes depending on the period type"""
        if not self.in_days:
            return self.period * 60  # 1 hour = 60 minutes

        return self.period * 1440  # 1 day = 1440 minutes
