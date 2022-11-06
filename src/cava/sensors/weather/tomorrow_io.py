from cava import log
from cava.models.tomorrow_io import weather_observation
import time

log = log()
log.info("Starting tomorrow.io sensor")
while True:  # We're gonna run forever!!!!
    current_observation = weather_observation.create_from_live_data()
    current_observation.log_observation()

    # Pass the result to Cava and then sleep
    current_observation.publish_to_cava()
    time.sleep(300)  # Sleep for 5 minutes
