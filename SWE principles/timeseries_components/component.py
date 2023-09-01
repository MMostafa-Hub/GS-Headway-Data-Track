from abc import ABC, abstractmethod
import pandas as pd


class Component(ABC):
    def __init__(self, time_series: pd.Series) -> None:
        """Initialize the component.

        Args:
            time_series (pd.Series): the time series to create the component from
        """
        self.time_series = time_series

    @property
    @abstractmethod
    def values(self) -> pd.Series:
        """Add a component to a time series."""
        pass
