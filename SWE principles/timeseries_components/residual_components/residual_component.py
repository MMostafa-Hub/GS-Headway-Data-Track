from abc import ABC, abstractmethod
import pandas as pd


class ResidualComponent(ABC):
    @abstractmethod
    @staticmethod
    def transform(time_series: pd.Series) -> pd.Series:
        pass
