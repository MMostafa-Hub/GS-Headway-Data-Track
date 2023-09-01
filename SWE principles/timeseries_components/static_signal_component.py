from component import Component
import pandas as pd


class StaticSignalComponent(Component):
    def __init__(self, time_series: pd.Series, magnitude: float) -> None:
        """Initialize the magnitude of the static signal component."""
        super().__init__(time_series)
        self.magnitude = magnitude

    @property
    def values(self) -> pd.Series:
        """Add static signal component to a time series."""
        return pd.Series()


ssc = StaticSignalComponent(pd.Series(), 1.0)
