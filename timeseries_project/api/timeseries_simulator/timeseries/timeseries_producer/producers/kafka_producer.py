from typing import override
import pandas as pd
from .producer_interface import ProducerInterface
from confluent_kafka import Producer
import socket


class KafkaProducer(ProducerInterface):
    """
    A producer class for generating and saving data in a Kafka topic.
    """

    def __init__(self, topic: str, host: str = "localhost", port: int = 9092):
        """
        Initialize a KafkaProducer instance.

        Parameters:
        - topic (str): The Kafka topic to save the data to.
        - host (str): The Kafka bootstrap host.
        - port (int): The Kafka bootstrap port.
        """
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
        self.producer.produce(self.topic, time_series.to_json())
        self.producer.flush()
