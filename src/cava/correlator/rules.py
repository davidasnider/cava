from cava.models.correlation import base_rule, resolver_context, rule_types
import rule_engine

# This will be a list of instantiated classes, base_rule
rules = [
    # Is it snowing? If so, turn on the driveway heater
    base_rule(
        rule_engine.Rule("model.snowing", context=resolver_context),
        "turn_on_driveway_heater",
        rule_types.trigger,
    ),
]
