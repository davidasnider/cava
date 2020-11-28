from cava.messages.receiver import Receiver
import cava

log = cava.log()


def callback(ch, method, properties, body):

    log.debug(f"Received {body} on routing_key {method.routing_key}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():

    # Instantiate our receiver object
    receiver = Receiver(routingKey="incoming.*", queue_name="correlator")

    # Connect to rabbitmq and associate the callback function
    receiver.connect(callback)

    # Start processing messages
    receiver.consume()


if __name__ == "__main__":
    main()
