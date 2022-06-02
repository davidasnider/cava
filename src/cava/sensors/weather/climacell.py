from cell_api.client import cellApiClient
import arrow
import time
import os
from cava.models.cell import weather_forecast as weather
from cava.models.cell import observation as observation
import requests
import cava

log = cava.log()
url = os.getenv("CAVA_URL")
uri = "/api/v01/weather"
key = os.getenv("CELL_API_KEY")
if key is None:
    print("You must specify an api key in the environment variable CEL_API_KEY")
    exit(255)

client = cellApiClient(key)
lat = "40.571710"
lon = "-111.791090"


def log_results(forecast_type, measurements, obs_time):
    output = f"{forecast_type}: {obs_time.to('America/Denver').ctime()} "
    output += f"Precipitation: {measurements['precipitation'].value} "
    output += f"Type: {measurements['precipitation_type'].value} "
    output += f"Weather: {measurements['weather_code'].value} "
    output += f"Temp: {measurements['temp'].value} "
    output += f"Visibility: {measurements['visibility'].value} "
    output += f"Cloud Cover: {measurements['cloud_cover'].value} "
    output += f"Cloud Base: {measurements['cloud_base'].value} "
    output += f"Cloud Ceiling: {measurements['cloud_ceiling'].value} "
    log.info(output)


def get_dict_values(measurements, observation_time) -> dict:
    log.debug("creating dictionary from result")
    return_dict = {
        "precipitation": measurements["precipitation"].value,
        "precipitation_type": measurements["precipitation_type"].value,
        "weather_code": measurements["weather_code"].value,
        "temp": measurements["temp"].value,
        "visibility": measurements["visibility"].value,
        "cloud_cover": measurements["cloud_cover"].value,
        "cloud_base": measurements["cloud_base"].value,
        "cloud_ceiling": measurements["cloud_ceiling"].value,
        "observation_time": arrow.get(observation_time).datetime,
    }
    log.debug(f"dictionary created: {return_dict}")
    return return_dict


my_fields = [
    "precipitation",
    "precipitation_type",
    "weather_code",
    "temp",
    "visibility",
    "cloud_cover",
    "cloud_base",
    "cloud_ceiling",
]

while True:
    log.debug("Getting forecast data from cell")
    n = client.nowcast(units="us", lat=lat, lon=lon, timestep=60, fields=my_fields)

    if n.status_code in [200]:
        log.debug("Weather successfully retrieved")
        # We have a good reponse

        # The first item is the current weather
        nowcast = n.data()[0].measurements
        nowcast_time = arrow.get(n.data()[0].observation_time)
        current_conditions = observation(**get_dict_values(nowcast, nowcast_time))
        log_results("Current", nowcast, nowcast_time)

        # The second is one hour from now
        nowcast = n.data()[1].measurements
        nowcast_time = arrow.get(n.data()[1].observation_time)
        future_conditions = observation(**get_dict_values(nowcast, nowcast_time))
        log_results("Forecast", nowcast, nowcast_time)

        weather_forcast = weather(
            current_conditions=current_conditions, future_conditions=future_conditions
        )

        result = requests.put(url + uri, weather_forcast.json())
        if result.ok:
            log.info("Result posted to cava")
        else:
            log.info(f"Failed to post to cava, error code: {result.status_code}")
    else:
        log.info(f"Failed to get data from cell, error code: {n.status_code}")

    time.sleep(900)
