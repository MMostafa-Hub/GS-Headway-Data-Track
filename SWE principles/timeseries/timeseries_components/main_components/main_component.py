from abc import ABC, abstractmethod
import pandas as pd


class MainComponent(ABC):
    def __init__(self, time_index: pd.DatetimeIndex) -> None:
        """Initialize the component.

        Args:
            time_series (pd.Series): the time series to create the component from
        """
        self.time_index = time_index

    @property
    @abstractmethod
    def values(self) -> pd.Series:
        """Add a component to a time series."""
        pass
