from .generator import Generator
import pandas as pd
import numpy as np


class SeasonalityGenerator(Generator):
    def __init__(
        self,
        period: int,
        amplitude: int = 1,
        in_days: bool = True,
        phase_shift: float = 0.0,
        multiplier: float = 1.0,
    ) -> None:
        """Initialize the period of the seasonality component.
        Args:
            period (int): the period of the seasonality component
            amplitude (int): the amplitude of the seasonality component
            in_days (bool): if True, the period is in days, otherwise in hours
            phase_shift (float): the phase shift of the seasonality component in radians
            multiplier (float): the multiplier for the seasonality component
        """
        super().__init__()
        self.period = period
        self.amplitude = amplitude
        self.in_days = in_days
        self.phase_shift = phase_shift
        self.multiplier = multiplier

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """
        Generates a sinusoidal seasonality component for a time series.

        Args:
            time_index (pd.DatetimeIndex): A DatetimeIndex representing the time points
                for which the seasonality component should be generated.

        Returns:
            pd.Series: A pandas Series representing the generated sinusoidal seasonality component.

        The seasonality component is generated as a sinusoidal wave with customizable
        amplitude, frequency (multiplier), and phase shift. It is calculated using the
        formula:

        amplitude * sin(2 * pi * time / total_period + phase_shift)

        where:
        - amplitude: The amplitude of the sinusoidal wave.
        - time: A sequence of numbers representing the position in the time_index.
        - total_period: The total number of time points in the seasonality cycle.
        - phase_shift: The phase shift (in radians) applied to the sinusoidal wave.
        """
        # sequence of numbers from 0 to the number of timestamps
        time = np.arange(len(time_index))

        return pd.Series(
            self.multiplier
            * (
                self.amplitude
                * np.sin(2 * np.pi * time / self.__total_period + self.phase_shift)
            )
        )

    @property
    def __total_period(self) -> int:
        """Convert the total period to minutes depending on the period type"""
        if not self.in_days:
            return self.period * 60  # 1 hour = 60 minutes

        return self.period * 1440  # 1 day = 1440 minutes
