"""
Single function, reads metrics from a queue and publishes to
InfluxDB
"""

# import json
import pika
import logging

# import jsonschema
import funcs
import os

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


# def callback(channel, delivery, properties, payload):
#     if funcs.is_valid_json(payload):
#         print(str(payload))


def main():

    # Connect to RabbitMQ
    password = os.getenv("CAVA_PASS")
    credentials = pika.PlainCredentials("cava", password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672, "/", credentials)
    )
    channel = connection.channel()

    # Get connected to RabbitMQ
    queue = "metrics"
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    # Read messages from the queue
    channel.start_consuming()

    # Validate the item is in fact a metric object

    # Log to Influx after collecting a few, or after a few seconds


main()
