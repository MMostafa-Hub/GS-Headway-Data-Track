import pandas as pd
from typing import List

from .timeseries_components.transformers.transformer import (
    Transformer,
)
from .timeseries_components.generators.generator import Generator
from operator import mul, add
from functools import reduce
from dataclasses import dataclass


@dataclass
class TimeSeriesParams:
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    frequency: str
    main_components: List[Generator]
    residual_components: List[Transformer]
    multiplicative: bool = True


class TimeSeriesGenerator:
    def __init__(
        self,
        time_series_params: TimeSeriesParams,
    ) -> None:
        """Initialize the time series generator."""
        self.start_date = time_series_params.start_date
        self.end_date = time_series_params.end_date
        self.frequency = time_series_params.frequency
        self.multiplicative = time_series_params.multiplicative
        self.main_components = time_series_params.main_components
        self.residual_components = time_series_params.residual_components

        # Creating the time index
        self.time_index = pd.date_range(
            start=self.start_date, end=self.end_date, freq=self.frequency
        )

    def generate(self) -> pd.Series:
        """Generates a time series based on the main and residual components."""
        # Choosing the operation to be performed based on the time series type
        operation = mul if self.multiplicative else add

        # Applying the main components
        result_series = pd.Series(
            reduce(
                lambda x, y: operation(x, y),
                [mc.generate(self.time_index) for mc in self.main_components],
            )
        )

        # Applying the residual components
        for rc in self.residual_components:
            result_series = rc.transform(result_series)

        return result_series
