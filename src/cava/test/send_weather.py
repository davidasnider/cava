from cava.models.climacell import weather_forecast

import requests
import time

url = "http://localhost:8000"
uri = "/api/v01/weather"

not_snowing = {
    "current_conditions": {
        "precipitation": 0.0,
        "precipitation_type": "none",
        "weather_code": "clear",
        "temp": 32.94,
        "visibility": 6.21,
        "cloud_cover": 0.0,
        "cloud_base": None,
        "cloud_ceiling": None,
        "observation_time": "2020-11-29T19:10:49.123000+00:00",
    },
    "future_conditions": {
        "precipitation": 0.0,
        "precipitation_type": "none",
        "weather_code": "clear",
        "temp": 34.59,
        "visibility": 6.21,
        "cloud_cover": 0.0,
        "cloud_base": None,
        "cloud_ceiling": None,
        "observation_time": "2020-11-29T20:10:49.123000+00:00",
    },
}


my_weather = weather_forecast(**not_snowing)
x = 1
while True:
    if x % 5 == 0:
        # Make it snow
        my_weather.current_conditions.weather_code = "snow"
        my_weather.current_conditions.precipitation = 0.2
    result = requests.put(url + uri, my_weather.json())
    time.sleep(1)
    x += 1

print(result)
