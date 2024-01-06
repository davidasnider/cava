from cava.messages.receiver import Receiver
from cava.models.correlation import (
    event_details,
    tracked_events,
)
from cava.correlator.rules import rules
import time
import cava
from pika.exceptions import AMQPConnectionError


log = cava.log()


# Initialize our tracked events, this is essentially our work list
our_tracked_events = tracked_events(rules)


def callback(ch, method, properties, body):
    log.debug(f"Received {body} on routing_key {method.routing_key}")

    # instantiate the appropriate class
    this_event_details = event_details(routingKey=method.routing_key, body=body)

    our_tracked_events.add_event(this_event_details)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Instantiate our receiver object
    receiver = Receiver(routingKey="incoming.*", queue_name="correlator")

    # Connect to rabbitmq and associate the callback function
    retries = 0
    while retries < 5:
        try:
            receiver.connect()
        except AMQPConnectionError as e:
            log.warning("rabbitmq connection failed, retry in 5 seconds")
            log.debug(f"exception is {e}")
            time.sleep(5)
            retries += 1
        else:
            break

    if retries == 5:
        log.error("Unable to connect to rabbitmq, quitting")
        exit()

    # Start processing messagessdk
    receiver.consume(callback)


if __name__ == "__main__":
    main()
