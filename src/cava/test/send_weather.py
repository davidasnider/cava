from cava.models.tomorrow_io import weather_observation

import requests
import time

url = "http://cava.thesniderpad.com:8000"
uri = "/api/v01/weather"

not_snowing = {
    "current_conditions": {
        "temperature": 32.94,
        "humidity": 20.0,
        "snowIntensity": 0.0,
        "snowAccumulation": 0.0,
        "precipitationType": "none",
    },
    "future_conditions": {
        "temperature": 32.94,
        "humidity": 20.0,
        "snowIntensity": 0.0,
        "snowAccumulation": 0.0,
        "precipitationType": "none",
    },
}


x = 1
while True:
    my_weather = weather_observation(**not_snowing)

    if x % 5 == 0:
        print("Snowing sent")
        # Make it snow
        my_weather.current_conditions.snow_intensity = 2
        my_weather.current_conditions.snow_accumulation = 2
    else:
        print("Not snowing sent")
    result = requests.put(url + uri, my_weather.json(by_alias=True))
    time.sleep(1)
    x += 1

print(result)
