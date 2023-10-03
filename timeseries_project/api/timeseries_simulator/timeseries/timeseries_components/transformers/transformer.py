from abc import ABC, abstractmethod
import pandas as pd


class Transformer(ABC):
    @abstractmethod
    def transform(self, time_series: pd.Series) -> pd.Series:
        """
        Abstract base class for time series transformers.

        This abstract class defines the interface for time series transformers. Subclasses
        should implement the 'transform' method to apply specific transformations to
        time series data.

        Args:
            time_series (pd.Series): The input time series data to be transformed.

        Returns:
            pd.Series: A pandas Series representing the transformed time series data.

        Subclasses should implement this method to define their own data transformation logic.
        """
