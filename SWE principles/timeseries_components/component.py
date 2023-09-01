from abc import ABC, abstractmethod
import pandas as pd


class Component(ABC):
    @abstractmethod
    def add(self, time_series: pd.Series) -> pd.Series:
        """Add a component to a time series."""
        pass
