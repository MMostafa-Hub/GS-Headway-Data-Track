from confluent_kafka import Consumer, KafkaException
import json
import pandas as pd

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "timeseries_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)


def print_assignment(consumer, partitions):
    print("Successfully Assigned to:", *partitions)


topic = "sink_topic"

# Subscribe to topic
consumer.subscribe([], on_assign=print_assignment)

# Timeseries dataframe to store the data from the Kafka topic
timeseries_df = pd.DataFrame(
    columns=["attribute_name", "value", "timestamp", "asset_name"]
)

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Append the message to the time series dataframe
            new_record = pd.DataFrame([dict(json.loads(msg.value().decode("utf-8")))])
            timeseries_df = pd.concat([timeseries_df, new_record], ignore_index=True)

except KeyboardInterrupt:
    pass

finally:
    # Save the time series dataframe to a csv file
    timeseries_df.to_csv("timeseries.csv")

    # Close down consumer to commit final offsets.
    consumer.close()
