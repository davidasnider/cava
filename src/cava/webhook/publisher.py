import pika
import traceback
import logging
import pathlib

LOGGING_CONFIG = pathlib.Path(__file__).parent.parent / "logging.conf"
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project
# This will get the root logger since no logger in the configuration has this name.


class Publisher:
    """
    Required keys

    * exchangeName
    * userName
    * password
    * host
    * port
    * virtualHost
    """

    def __init__(self, config):
        self.config = config

    def publish(self, message, routingKey="metrics"):
        connection = None
        logging.debug(f"attempting publish of: {message}")

        try:
            connection = self._create_connection()
            channel = connection.channel()
            logging.debug("connection complete")
            channel.exchange_declare(
                exchange=self.config["exchangeName"], exchange_type="topic"
            )
            logging.debug(f"publishing {message} to {routingKey}")
            channel.basic_publish(
                exchange=self.config["exchangeName"],
                routing_key=routingKey,
                body=message,
            )

            # print(" [x] Sent message %r" % message)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()

    def _create_connection(self):
        logging.debug(f"creating connection {self.config}")
        credentials = pika.PlainCredentials(
            self.config["userName"], self.config["password"]
        )
        parameters = pika.ConnectionParameters(
            self.config["host"],
            self.config["port"],
            self.config["virtualHost"],
            credentials,
        )

        logging.debug(f"creating connection {self.config}")
        return pika.BlockingConnection(parameters)
