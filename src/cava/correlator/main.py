from cava.messages.receiver import Receiver
from cava.models.correlation import (
    event_details,
    tracked_events,
)
from cava.correlator.rules import rules
import time
import cava

log = cava.log()


# Initialize our tracked events, this is essentially our work list
our_tracked_events = tracked_events(rules)


def callback(ch, method, properties, body):

    log.debug(f"Received {body} on routing_key {method.routing_key}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # instantiate the appropriate class
    this_event_details = event_details(routingKey=method.routing_key, body=body)

    our_tracked_events.add_event(this_event_details)


def main():

    # Instantiate our receiver object
    receiver = Receiver(routingKey="incoming.*", queue_name="correlator")

    # Connect to rabbitmq and associate the callback function
    retries = 0
    while retries < 5:
        try:
            receiver.connect()
        except Exception as e:
            log.info("rabbitmq connection failed, retry in 5 seconds")
            log.debug(f"exception is {e}")
            time.sleep(5)
            retries += 1
        else:
            break

    if retries == 5:
        log.info("Unable to connect to rabbitmq, quitting")
        exit()

    # Start processing messages
    receiver.consume(callback)


if __name__ == "__main__":
    main()
