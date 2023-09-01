from component import Component
import pandas as pd


class TrendComponent(Component):
    def __init__(
        self, time_series: pd.Series, magnitude: float, negative: bool = False
    ) -> None:
        """Initialize the magnitude and direction of the trend component.

        Args:
            magnitude (float): the magnitude of the trend component
            negative (bool, optional): Defaulting the trend to be positive.
        """
        super().__init__(time_series)
        self.magnitude = magnitude
        self.direction = -1 if negative else 1

    @property
    def values(self) -> pd.Series:
        """Add the trend component to a time series."""
        return pd.Series()
