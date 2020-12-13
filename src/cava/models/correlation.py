from cava.models.amcrest import event as motion_event
from cava.models.climacell import weather_forecast
import json
import arrow
from enum import Enum
import cava
import rule_engine
from cava.messages.publisher import Publisher

log = cava.log()


# Define the types of rules we want to process. Trigger happens with a single
# event, multi_condition searches all events
class rule_types(str, Enum):
    trigger = "trigger"
    multi_condition = "multi_condition"


# A base rule has information about the type of rule. what action to take when
# found, and whether it is a trigger or multi-condition rule
class base_rule:
    def __init__(self, test, action: str, rule_type: rule_types):
        self._test = test
        self._action = action
        self._type = rule_type

    @property
    def test(self):
        return self._test

    @property
    def action(self):
        return self._action

    @property
    def type(self):
        return self._type


# This context is used when we want to analyze python objects
resolver_context = rule_engine.Context(resolver=rule_engine.resolve_attribute)

event_to_class_map = {
    "incoming.motion": motion_event,
    "incoming.weather": weather_forecast,
}


class event_details:
    def __init__(self, routingKey, body):
        self._routingKey = routingKey
        self._body = body
        self.matched = False

        # convert body from bytecode to dictionary
        body_dict = json.loads(body.decode())
        self.model = event_to_class_map[routingKey](**body_dict)
        self.timestamp = arrow.now()

        log.info(f"stored event for {routingKey}")


class tracked_events:
    def __init__(self, rules):
        self.events = []
        self.rules = rules
        self.publisher = Publisher()

    def add_event(self, event: event_details):
        self.events.append(event)
        log.info(f"currently storing {len(self.events)}")

        # process expired
        # Todo this should be a thread running on a schedule
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

    def process_rules(self) -> bool:

        # Run trigger rules against current item
        for rule in self.rules:
            if rule.type == rule_types.trigger:
                matches = False
                # Without the try, the rule will get an attribute error when the
                # rule attribute does not exits
                try:
                    matches = rule.test.matches(self.events[-1])
                except Exception:
                    log.debug(
                        f"did not match {self.events[-1]._routingKey} to {rule.action}"
                    )
                if matches:
                    self.events[-1].matched = True
                    log.info(f"matched {self.events[-1]._routingKey} to {rule.action}")
                    log.debug(f"rule criteria: {rule.test.text}")

                    # We'll do some sort of submit here.
                    self.publisher.publish(rule.action, "run.action")

        # Process all the rules
        # rule.filter(self.events) # Todo, this doesn't work right now
