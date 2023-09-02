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
        main_components: List[MainComponent],
        residual_components: List[ResidualComponent],
        multiplicative: bool = True,
    ) -> None:
        self.multiplicative = multiplicative
        self.main_components = main_components
        self.residual_components = residual_components

    def generate(self) -> pd.Series:
        # Choosing the operation to be performed based on the time series type
        operation = mul if self.multiplicative else add
        
        # Applying the main components
        result_series = pd.Series(
            reduce(operation, [mc.values for mc in self.main_components])
        )
        
        # Applying the residual components
        for rc in self.residual_components:
            result_series = rc.transform(result_series)

        return result_series
