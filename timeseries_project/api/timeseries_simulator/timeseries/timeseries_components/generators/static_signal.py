from .generator import Generator
import pandas as pd
import numpy as np


class StaticSignalGenerator(Generator):
    def __init__(self, magnitude: float) -> None:
        """Initialize the magnitude of the static signal component."""
        super().__init__()
        self.magnitude = magnitude

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """
        Generate a static signal component for a time series.

        Args:
            time_index (pd.DatetimeIndex): A DatetimeIndex representing the time points
                for which the static signal component should be generated.

        Returns:
            pd.Series: A pandas Series representing the generated static signal component.

        This method generates a static signal component that remains constant across all
        time points specified in the 'time_index'. The static signal component is defined
        by a magnitude value, which determines the constant value of the signal.

        Args:
        - time_index: A DatetimeIndex specifying the time points for the generated signal.

        Returns:
        - pd.Series: A pandas Series with constant values equal to 'self.magnitude' and
        indexed by the provided 'time_index'.
        """
        return pd.Series(
            np.ones(time_index.shape[0]) * self.magnitude, index=time_index
        )
