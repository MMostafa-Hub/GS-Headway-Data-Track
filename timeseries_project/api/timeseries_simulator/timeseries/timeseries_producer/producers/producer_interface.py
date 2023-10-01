from abc import ABC, abstractmethod
import pandas as pd


class ProducerInterface(ABC):
    @abstractmethod
    def produce(self, time_series: pd.Series):
        pass
