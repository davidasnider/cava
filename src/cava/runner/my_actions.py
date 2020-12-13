from cava.runner.actions import action, actions, indigo_executor, influxdb_executor


# Create executors that do a thing
indigo_turn_on_driveway = indigo_executor(uri="/actions/Melt%20Driveway%201%20Hour")
metrics_turn_on_driveway = influxdb_executor(
    metric_name="cava_turn_on_driveway", metric=1
)

# Create actions that tie actions to executors
turn_on_driveway_heater = action(
    name="indigo_turn_on_driveway",
    action="turn_on_driveway_heater",
    executor=indigo_turn_on_driveway,
)
turn_on_driveway_heater_metric = action(
    name="metric_turn_on_driveway",
    action="turn_on_driveway_heater",
    executor=metrics_turn_on_driveway,
)

# Initialize our list of actions
rules_to_actions = actions()

# add newly created actions to the rules_to_actions
rules_to_actions.action_list.append(turn_on_driveway_heater)
rules_to_actions.action_list.append(turn_on_driveway_heater_metric)
