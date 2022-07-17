import cava
from cava.models.tomorrow_io import weather_observation
import time

log = cava.log()

while True:  # We're gonna run forever!!!!
    log.info("Getting forecast data from tomorrow.io")
    current_observation = weather_observation.create_from_live_data()
    current_observation.log_observation()

    # Pass the result to Cava and then sleep
    current_observation.publish_to_cava()
    time.sleep(300)  # Sleep for 5 minutes
