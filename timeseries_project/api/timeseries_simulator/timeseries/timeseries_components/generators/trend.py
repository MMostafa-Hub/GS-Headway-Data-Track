from .generator import Generator
import pandas as pd
import numpy as np
from typing import List


class TrendGenerator(Generator):
    def __init__(self, coefficients: List[float] = (1.0,)) -> None:
        """Initialize the coefficients of the trend component.

        Args:
            coefficients (List[float]): The coefficients of the polynomial, in descending order.
                         For example, [a, b, c] corresponds to a*t^2 + b*t + c.
                         where t is the time index.
        """
        super().__init__()
        self.coefficients = coefficients

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """
        Generate the trend component for a time series.

        Args:
            time_index (pd.DatetimeIndex): A DatetimeIndex representing the time points
                for which the trend component should be generated.

        Returns:
            pd.Series: A pandas Series representing the generated trend component.

        This method generates the trend component of a time series using polynomial regression.
        The trend component represents the long-term, systematic variation in the time series.

        Args:
        - time_index: A DatetimeIndex specifying the time points for the generated trend component.

        Returns:
        - pd.Series: A pandas Series containing the trend component values corresponding to
        the provided 'time_index'. The trend is computed using the polynomial coefficients
        defined in 'self.coefficients'.
        """

        # sequence of numbers from 0 to the number of timestamps
        time = np.arange(len(time_index))
        return pd.Series(np.polyval(self.coefficients, time))
