from abc import ABC, abstractmethod
import pandas as pd


class ProducerInterface(ABC):
    @abstractmethod
    def produce(self, time_series: pd.Series):
        """
        Abstract base class for time series producers.

        This abstract class defines the interface for time series producers. Subclasses
        should implement the 'produce' method to write or output time series data in
        a specific format or destination.

        Args:
            time_series (pd.Series): The time series data to be produced or written.

        Subclasses should implement this method to define their own logic for producing
        or writing time series data to a particular format or destination.
        """
