import json
import rule_engine
from cava.models.correlation import (
    event_details,
    tracked_events,
    base_rule,
    rule_types,
)


def test_event_details_snowing(setup_module, weather_json):
    context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
    re_rule = rule_engine.Rule("model.snowing", context=context)
    my_rule = base_rule(re_rule, "turn_on_driveway_heater", rule_types.trigger)
    rules = [my_rule]
    weather_json["current_conditions"]["precipitationType"] = "snow"
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
