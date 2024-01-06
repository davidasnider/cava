import datetime
import json
import time

import cava
import requests
from cava.models.settings import Settings
from pydantic import BaseModel, Field

log = cava.log()
settings = Settings()


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
            "location": [
                settings.TOMORROW_IO_LATITUDE,
                settings.TOMORROW_IO_LONGITUDE,
            ],  # Our house
            "timezone": settings.TZ,
            "fields": list(
                individual_observation.model_json_schema()["properties"].keys()
            ),  # Get the list of fields from the class itself
        }
        api_url = "https://api.tomorrow.io/v4/timelines/"
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": settings.TOMORROW_IO_API_KEY.get_secret_value(),
        }

        while True:  # Just keep trying until we get a response
            response = requests.post(
                api_url, data=json.dumps(payload_defaults), headers=header
            )

            if response.ok:
                # Get to just the interval data that we want.
                my_weather_data_raw = response.json()["data"]["timelines"][0][
                    "intervals"
                ]

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
                log.info(
                    f"Received new observation: Temp - {new_observation.current_conditions.temperature}"
                )
                return new_observation

            elif response.status_code == 429:
                print(
                    f"Too many requests retry after {response.headers['Retry-After']} seconds"
                )
                # Sleep for how long the Retry-After header tells us, plus one second
                time.sleep(int(response.headers["Retry-After"]) + 1)
            else:
                log.error(
                    f"Failed to get weather data from tomorrow.io, error code: {response.status_code}"
                )
                time.sleep(60)  # Sleep for 1 minutes

    def log_observation(self):
        log.info(f"Current conditions: {self.current_conditions}")
        log.info(f"Future conditions: {self.future_conditions}")

    def publish_to_cava(self):
        url = settings.CAVA_URL
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

    @property
    def snowing(self):
        """
        Returns true if snowIntensity is > 1 inch for the current observation
        or if future conditions show > 1 inch of accumulation

        see https://docs.tomorrow.io/reference/data-layers-core for the description
        of the snowIntensity field.
        """
        return_value = (self.current_conditions.snow_intensity > 1) or (
            self.future_conditions.snow_accumulation > 1
        )
        return return_value
