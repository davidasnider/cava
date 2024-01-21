import json
import pytest
import rule_engine
from cava.models.correlation import (
    event_details,
    tracked_events,
    base_rule,
    rule_types,
)
from unittest.mock import Mock, patch
from cava.correlator.main import callback, connect_receiver
from pika.exceptions import AMQPConnectionError


@pytest.mark.integration
def test_event_details_snowing(setup_module, weather_json):
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    re_rule = rule_engine.Rule("model.snowing", context=context)
    my_rule = base_rule(re_rule, "turn_on_driveway_heater", rule_types.trigger)
    rules = [my_rule]
    weather_json["current_conditions"]["precipitationType"] = 2  # 2 = Snow
    weather_json["current_conditions"]["snowIntensity"] = 1.5
    test_event = event_details(
        "incoming.weather", str(json.dumps(weather_json)).encode()
    )
    my_tracked_events = tracked_events(rules)
    my_tracked_events.add_event(test_event)
    assert my_tracked_events.events[-1].matched


def test_event_details_snowing_fail(weather_json):
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    re_rule = rule_engine.Rule("model.snowing", context=context)
    my_rule = base_rule(re_rule, "turn_on_driveway_heater", rule_types.trigger)
    rules = [my_rule]
    test_event = event_details(
        "incoming.weather", str(json.dumps(weather_json)).encode()
    )
    my_tracked_events = tracked_events(rules)
    my_tracked_events.add_event(test_event)
    assert my_tracked_events.events[-1].matched is False


def test_base_rule_string():
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    re_rule = rule_engine.Rule("model.snowing", context=context)
    my_rule = base_rule(re_rule, "turn_on_driveway_heater", rule_types.trigger)
    assert my_rule.test == re_rule
    assert my_rule.action == "turn_on_driveway_heater"


def test_callback(amcrest_json):
    # Create mock objects for the parameters
    ch = Mock()
    method = Mock()
    properties = Mock()

    # Set the routing_key attribute of the method mock object
    method.routing_key = "incoming.motion"

    # Make it a byte string
    body = str(json.dumps(amcrest_json)).encode()

    # Call the function with the mock objects
    callback(ch, method, properties, body)

    # Check that the basic_ack method was called on the channel mock object
    ch.basic_ack.assert_called_once()


def test_connect_receiver_success():
    # Create a mock receiver object
    receiver = Mock()

    # Call the function with the mock receiver
    connect_receiver(receiver)

    # Check that the connect method was called on the receiver mock object
    receiver.connect.assert_called_once()


@patch("cava.correlator.main.log")
def test_connect_receiver_failure(mock_log):
    # Create a mock receiver object that raises an AMQPConnectionError when connect is called
    receiver = Mock()
    receiver.connect.side_effect = AMQPConnectionError

    # Call the function with the mock receiver and check that it raises an AMQPConnectionError
    with pytest.raises(AMQPConnectionError):
        connect_receiver(receiver, max_retries=1)

    # Check that the warning and error methods were called on the log mock object
    mock_log.warning.assert_called_once_with(
        "rabbitmq connection failed, retry in 5 seconds"
    )
    mock_log.error.assert_called_once_with("Unable to connect to rabbitmq, quitting")
