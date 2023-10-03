from abc import ABC, abstractmethod
import pandas as pd


class Generator(ABC):
    @abstractmethod
    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """
        Abstract method for generating a time series component.

        This method should be implemented by concrete subclasses to generate
        a specific time series component (e.g., trend, seasonality).

        Args:
            time_index (pd.DatetimeIndex): A DatetimeIndex representing the time points
                for which the time series component should be generated.

        Returns:
            pd.Series: A pandas Series representing the generated time series component.
        """
