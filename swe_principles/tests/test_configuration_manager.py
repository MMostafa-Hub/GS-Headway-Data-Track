from unittest import TestCase
from ..timeseries.configuration_manager import ConfigurationManager
from ..timeseries.timeseries_simulator import TimeSeriesParams


class TestConfigurationManager(TestCase, ConfigurationManager):
    def test_public_params_missing_keys(self):
        """Tests that the __params method raises a KeyError when the configuration dictionary is missing keys."""
        incomplete_config_data = {
            "time_index": {
                "start_date": "2019-01-01",
                "end_date": "2023-01-01",
                "sampling_frequency_in_minutes": 60,  # 1 hour
            },
            "multiplicative": True,
            # Missing main_components
        }
        with self.assertRaises(KeyError):
            self.__params(incomplete_config_data)

    def test__params_success(self):
        import pandas as pd

        config = {
            "time_index": {
                "start_date": "2019-01-01",
                "end_date": "2023-01-01",
                "sampling_frequency_in_minutes": 60,  # 1 hour
            },
            "multiplicative": True,
            "main_components": {
                "trend": {
                    "coefficients": [0.005, 0.001],
                },
                # You can add more than one seasonality component
                "seasonality": [
                    {"in_days": False, "period": 24, "amplitude": 0.5},  # Daily
                    {"in_days": True, "period": 365, "amplitude": 0.005},  # Yearly
                ],
            },
            "residual_components": {
                "noise": {"noise_level": 0.1},
                "outliers": {"outlier_ratio": 0.001},
            },
        }
        time_series_params = self.__params(config)
        # Testing the type of the returned object
        self.assertIsInstance(time_series_params, TimeSeriesParams)

        # Testing the time index
        self.assertEqual(
            time_series_params.time_index,
            pd.date_range(start="2019-01-01", end="2023-01-01", freq="60T"),
        )

        # Testing the multiplicative flag
        self.assertTrue(time_series_params.multiplicative)
