from cava.messages.receiver import Receiver
from cava.models.amcrest import event as motion_event
from cava.models.climacell import weather_forecast
import json
import arrow

import cava

log = cava.log()


rule = [
    # see https://zerosteiner.github.io/rule-engine/
]

event_to_class_map = {
    "incoming.motion": motion_event,
    "incoming.weather": weather_forecast,
}


class event_details:
    def __init__(self, routingKey, body):
        self._routingKey = routingKey
        self._body = body

        # convert body from bytecode to dictionary
        body_dict = json.loads(body.decode())
        self.model = event_to_class_map[routingKey](**body_dict)
        self.timestamp = arrow.now()

        log.info(f"stored event for {routingKey}")


class tracked_events:
    def __init__(self):
        self.events = []

    def add_event(self, event: event_details):
        self.events.append(event)
        log.info(f"currently storing {len(self.events)}")

        # process expired
        self.purge_expired()

        # Todo trigger rules
        self.process_rules()

    def purge_expired(self):
        # Simply remove anything older than a constant age at the moment
        x = 0
        current_time = arrow.now()
        while self.events[x].timestamp < current_time.shift(minutes=-2):
            x += 1

        del self.events[:x]
        log.info(f"deleted {x} expired events")

    def process_rules(self):
        # Process all the rules
        pass


# Initialize our tracked events, this is essentially our work list
our_tracked_events = tracked_events()


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
    receiver.connect()

    # Start processing messages
    receiver.consume(callback)


if __name__ == "__main__":
    main()
