"""
Reads all of the logs on the message exchange, useful for testing inputs
"""

import pika
from cava.models.settings import Settings

settings = Settings()


def callback(channel, method, properties, body):  # dead: disable
    """
    stdout print of incoming messages
    """
    # We don't use either of these, so delete them
    del channel
    del properties

    print(" [x] %r:%r" % (method.routing_key, str(body)))


def main():
    """
    Main program for reading logs
    """

    password = settings.CAVA_PASSWORD.get_secret_value()
    credentials = pika.PlainCredentials("cava", password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("10.9.11.1", 5672, "/", credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="message_exchange", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "*"

    channel.queue_bind(
        exchange="message_exchange", queue=queue_name, routing_key=binding_key
    )

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


# Run main program
main()
