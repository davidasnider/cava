import pika
import traceback
import cava
from cava.models.settings import Settings

log = cava.log()

settings = Settings()


class Publisher:
    # Configuration parameters for RabbitMQ
    def __init__(self):
        self._config = {
            "exchangeName": "message_exchange",
            "userName": settings.RABBITMQ_DEFAULT_USER,
            "password": settings.RABBITMQ_DEFAULT_PASS.get_secret_value(),
            "host": settings.RABBITMQ_SERVICE_SERVICE_HOST,
            "port": "5672",
            "virtualHost": "/",
        }

        log.debug(f"RabbitMQ Config: {self._config}")

    def publish(self, message, routingKey="incoming"):
        connection = None
        log.debug(f"attempting publish of: {message}")

        try:
            connection = self._create_connection()
            channel = connection.channel()
            log.debug("connection complete")
            channel.exchange_declare(
                exchange=self._config["exchangeName"], exchange_type="topic"
            )
            log.debug(f"publishing {message} to {routingKey}")
            channel.basic_publish(
                exchange=self._config["exchangeName"],
                routing_key=routingKey,
                body=message,
            )

            # print(" [x] Sent message %r" % message)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            log.debug(f"error publishing message {e}")
            raise e
        finally:
            if connection:
                log.debug("closing connection to rabbitmq")
                connection.close()

    # This sets up our connections credentials and host/port info.
    def _create_connection(self):
        log.debug(f"creating credentials {self._config}")
        credentials = pika.PlainCredentials(
            self._config["userName"], self._config["password"]
        )
        parameters = pika.ConnectionParameters(
            self._config["host"],
            self._config["port"],
            self._config["virtualHost"],
            credentials,
        )

        log.debug(f"creating connection {self._config}")
        return pika.BlockingConnection(parameters)
