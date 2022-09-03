import pika
from cava import log
from cava.models.settings import Settings

log = log()
settings = Settings()


class Receiver:

    # Configuration parameters for RabbitMQ
    def __init__(self, routingKey="incoming.*", queue_name=None):

        self._config = {
            "exchangeName": "message_exchange",
            "userName": settings.RABBITMQ_DEFAULT_USER,
            "password": settings.RABBITMQ_DEFAULT_PASS.get_secret_value(),
            "host": settings.RABBITMQ_SERVICE_SERVICE_HOST,
            "port": "5672",
            "virtualHost": "/",
        }
        self.routingKey = routingKey
        self.queue_name = queue_name

        log.debug(f"RabbitMQ Config: {self._config}")

        if (
            self._config["userName"] is None
            or self._config["password"] is None
            or self._config["host"] is None
        ):
            log.warning("You must specify the proper environment variables")
            exit(255)

    def connect(self):

        credentials = pika.PlainCredentials(
            self._config["userName"], self._config["password"]
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self._config["host"], 5672, "/", credentials)
        )
        self.channel = connection.channel()

        self.channel.exchange_declare(
            exchange=self._config["exchangeName"], exchange_type="topic"
        )

        # Get a random queue for our collector if not specified
        if self.queue_name is None:
            # Generated queue names should be assumed to be exclusive
            result = self.channel.queue_declare("", exclusive=True)
            self.queue_name = result.method.queue
        else:
            result = self.channel.queue_declare(self.queue_name)

        self.channel.queue_bind(
            exchange=self._config["exchangeName"],
            queue=self.queue_name,
            routing_key=self.routingKey,
        )

        log.info(
            f"connected to exchange {self._config['exchangeName']}, queue {self.queue_name}, routing {self.routingKey}"
        )

    def consume(self, callback):

        self.callback = callback
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback
        )

        self.channel.start_consuming()
