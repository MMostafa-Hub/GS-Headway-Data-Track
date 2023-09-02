from abc import ABC, abstractmethod
import pandas as pd


class MainComponent(ABC):
    def __init__(self):
        self.time_index: pd.DatetimeIndex = pd.DatetimeIndex()

    @abstractmethod
    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Generates the time series component."""
        pass
