import pandas as pd
from .producer_interface import ProducerInterface


class CsvProducer(ProducerInterface):
    """
    A producer class for generating and saving data in a CSV file.
    """

    def __init__(self, identifier: str):
        """
        Initialize a CsvProducer instance.

        Parameters:
        - identifier (str): The file path or identifier for the CSV file.
        """
        self.identifier = identifier

    def produce(self, time_series: pd.Series):
        """
        Produce and save data as a Django model.

        Parameters:
        - time_series (pd.Series): The data to be saved in the Django model.

        Saves the provided data into a Django model specified by the 'identifier'
        attribute.
        """
        time_series.to_csv(self.identifier)
