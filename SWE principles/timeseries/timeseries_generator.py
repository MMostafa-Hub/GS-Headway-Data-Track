import pandas as pd
from typing import List
from timeseries_components.main_components.main_component import MainComponent
from timeseries_components.residual_components.residual_component import (
    ResidualComponent,
)
from operator import mul, add
from functools import reduce


class TimeSeriesGenerator:
    def __init__(
        self,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
        frequency: str,
        main_components: List[MainComponent],
        residual_components: List[ResidualComponent],
        multiplicative: bool = True,
    ) -> None:
        """Initialize the time series generator."""
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.multiplicative = multiplicative
        self.main_components = main_components
        self.residual_components = residual_components

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
