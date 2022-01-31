import datetime
import json
import os

import cava
import requests
from pydantic import BaseModel, Field

log = cava.log()

# We need these... if they don't exist, quit
required_variables = ["TOMORROW_IO_API_KEY", "CAVA_URL"]
for required_variable in required_variables:
    if required_variable not in os.environ:
        log.error(f"Missing required environment variable {required_variable}")
        exit(1)


class individual_observation(BaseModel):
    temperature: float
    humidity: float
    snow_intensity: float = Field(..., alias="snowIntensity")  # API is in camelCase
    precipitation_type: str = Field(..., alias="precipitationType")
    snow_accumulation: float = Field(..., alias="snowAccumulation")


class weather_observation(BaseModel):
    current_conditions: individual_observation
    future_conditions: individual_observation

    def create_from_live_data():
        """
        Get the current weather observation from the API. Defaults to two observations
        on for current and one hour from now. Returns type weather_observation
        """
        # Setup the queries
        observation_start_time = datetime.datetime.utcnow()
        observation_end_time = observation_start_time + datetime.timedelta(minutes=60)

        payload_defaults = {
            "units": "imperial",
            "startTime": observation_start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endTime": observation_end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "timesteps": ["1h"],
            "location": [40.571709, -111.791092],  # Our house
            "timezone": "America/Denver",
            "fields": list(
                individual_observation.schema()["properties"].keys()
            ),  # Get the list of fields from the class itself
        }
        api_url = "https://api.tomorrow.io/v4/timelines/"
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": os.getenv("TOMORROW_IO_API_KEY"),
        }

        response = requests.post(
            api_url, data=json.dumps(payload_defaults), headers=header
        )

        if response.ok:

            # Get to just the interval data that we want.
            my_weather_data_raw = response.json()["data"]["timelines"][0]["intervals"]

            # Get the current conditions
            api_current_conditions = individual_observation(
                **my_weather_data_raw[0]["values"]
            )

            # Get the future conditions
            api_future_conditions = individual_observation(
                **my_weather_data_raw[1]["values"]
            )

            new_observation = weather_observation(
                current_conditions=api_current_conditions,
                future_conditions=api_future_conditions,
            )
            return new_observation

        else:
            log.error(
                f"Failed to get weather data from tomorrow.io, error code: {response.status_code}"
            )
            return None

    def log_observation(self):
        log.info(f"Current conditions: {self.current_conditions}")
        log.info(f"Future conditions: {self.future_conditions}")

    def publish_to_cava(self):
        url = os.getenv("CAVA_URL")
        uri = "/api/v01/weather"
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        result = requests.put(url + uri, data=self.json(by_alias=True), headers=header)
        if result.ok:
            log.info("Published weather observation to CAVA")
        else:
            log.error(
                f"Failed to publish weather observation to CAVA, error code: {result.status_code}"
            )
