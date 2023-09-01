from component import Component
import pandas as pd


class SeasonalityComponent(Component):
    def __init__(
        self, time_series: pd.Series, period: int, in_days: bool = True
    ) -> None:
        """Initialize the period of the seasonality component.

        Args:
            period (int): the period of the seasonality component
            in_days (bool, optional): Defaulting the period to be in days.
        """
        super().__init__(time_series)
        self.period = period
        self.in_days = in_days

    @property
    def values(self) -> pd.Series:
        """Add seasonality component to a time series."""
        return pd.Series()
