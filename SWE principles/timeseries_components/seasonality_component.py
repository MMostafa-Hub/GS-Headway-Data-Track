from component import Component
import pandas as pd
import numpy as np
from enum import Enum


class SeasonalityPeriod(Enum):
    DAY = 1
    WEEK = 7
    MONTH = 30
    QUARTER = 90
    YEAR = 365


class SeasonalityComponent(Component):
    def __init__(self, time_index: pd.DatetimeIndex, period: SeasonalityPeriod) -> None:
        """Initialize the period of the seasonality component.

        Args:
            period (int): the period of the seasonality component in days
        """
        super().__init__(time_index)
        self.period = period

    @property
    def values(self) -> pd.Series:
        """Create seasonality component for a time series."""
        return pd.Series(np.sin(2 * np.pi * self.__total_period() / self.period.value))

    def __total_period(self):
        """Convert the total period to days or hours depending on the period"""
        if self.period == SeasonalityPeriod.DAY:
            return (self.time_index - self.time_index[0]).seconds / 3600
        else:
            return (self.time_index - self.time_index[0]).days
