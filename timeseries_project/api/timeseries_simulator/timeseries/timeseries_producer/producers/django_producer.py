from typing import override
import pandas as pd
from .producer_interface import ProducerInterface
from django.db import models


class DjangoModelProducer(ProducerInterface):
    """
    A producer class for generating and saving data in a Django model.
    """

    def __init__(self, identifier: str, model: models.Model):
        """
        Initialize a DjangoModelProducer instance.

        Parameters:
        - identifier (str): The model identifier.
        - model (models.Model): The Django model to save the data to.
        """
        self.identifier = identifier
        self.model = model

    @override
    def produce(self, time_series: pd.Series):
        """
        Produce and save data as a CSV file.

        Parameters:
        - data (pd.Series): The data to be saved in the CSV file.

        Saves the provided data into a CSV file specified by the 'identifier'
        attribute.
        """
        self.model.objects.filter(id=self.identifier).update(
            time_series=time_series.to_json()
        )
