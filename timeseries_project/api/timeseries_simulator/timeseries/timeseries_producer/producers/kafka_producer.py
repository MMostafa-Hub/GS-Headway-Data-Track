from dataclasses import dataclass
from typing import override
import pandas as pd
from .producer_interface import ProducerInterface
from confluent_kafka import Producer
import socket
from rest_framework.serializers import ModelSerializer
import json


@dataclass
class KafkaMessage:
    """A dataclass for that defines schema of the message sent to the Kafka topic."""

    attribute_name: str
    value: list
    timestamp: list
    asset_name: str


class KafkaProducer(ProducerInterface):
    """
    A producer class for generating and saving data in a Kafka topic.
    """

    def __init__(
        self,
        generator_name: str,
        attribute_name: str,
        topic: str,
        host: str = "localhost",
        port: int = 9092,
    ):
        """
        Initialize a KafkaProducer instance.

        Parameters:
        - generator_name (str): The name of the generator of the data.
        - attribute_name (str): The name of the attribute of the data.
        - topic (str): The Kafka topic to save the data to.
        - host (str): The Kafka bootstrap host.
        - port (int): The Kafka bootstrap port.
        """
        self.generator_name = generator_name
        self.attribute_name = attribute_name
        self.topic = topic
        self.producer = Producer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "client.id": socket.gethostname(),
            }
        )

    @override
    def produce(self, time_series: pd.Series):
        """
        Produce and save data as a Kafka topic.

        Parameters:
        - data (pd.Series): The data to be sent to the Kafka topic.

        Sends the provided data into a Kafka topic specified by the 'topic' attribute.
        """
        message = KafkaMessage(
            attribute_name=self.generator_name,
            value=time_series.values.tolist(),
            timestamp=time_series.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
            asset_name=self.attribute_name,
        )
        self.producer.produce(self.topic, json.dumps(message.__dict__).encode("utf-8"))
        self.producer.flush()
