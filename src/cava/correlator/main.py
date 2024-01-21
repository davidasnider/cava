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


def connect_receiver(receiver, max_retries=5, sleep_time=5):
    retries = 0
    e = None  # initialize exception variable
    while retries < max_retries:
        try:
            receiver.connect()
        except AMQPConnectionError as ex:
            e = ex  # Assign the exception for return later
            log.warning("rabbitmq connection failed, retry in 5 seconds")
            log.debug(f"exception is {e}")
            time.sleep(sleep_time)
            retries += 1
        else:
            break

    if retries == max_retries:
        log.error("Unable to connect to rabbitmq, quitting")
        if e is not None:
            raise e


def main():
    # Instantiate our receiver object
    receiver = Receiver(routingKey="incoming.*", queue_name="correlator")

    # Connect to rabbitmq and associate the callback function
    connect_receiver(receiver)

    # Start processing messagessdk
    receiver.consume(callback)


if __name__ == "__main__":
    main()
