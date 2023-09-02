from main_component import MainComponent
import pandas as pd
import numpy as np
from enum import Enum


class Period(Enum):
    DAY = 1
    WEEK = 7
    MONTH = 30
    QUARTER = 90
    YEAR = 365


class SeasonalityComponent(MainComponent):
    def __init__(self, period: Period) -> None:
        """Initialize the period of the seasonality component.

        Args:
            period (int): the period of the seasonality component in days
        """
        super().__init__()
        self.period = period

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        self.time_index = time_index
        """Create seasonality component for a time series."""
        return pd.Series(np.sin(2 * np.pi * self.__total_period() / self.period.value))

    def __total_period(self):
        """Convert the total period to days or hours depending on the period"""
        if self.period == Period.DAY:
            return (self.time_index - self.time_index[0]).seconds / 3600
        else:
            return (self.time_index - self.time_index[0]).days
