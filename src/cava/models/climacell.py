from pydantic import BaseModel
from typing import Optional
import cava
from enum import Enum
from datetime import datetime


log = cava.log()


class weather_codes(str, Enum):
    freezing_rain_heavy = "freezing_rain_heavy"
    freezing_rain = "freezing_rain"
    freezing_rain_light = "freezing_rain_light"
    freezing_drizzle = "freezing_drizzle"
    ice_pellets_heavy = "ice_pellets_heavy"
    ice_pellets = "ice_pellets"
    ice_pellets_light = "ice_pellets_light"
    snow_heavy = "snow_heavy"
    snow = "snow"
    snow_light = "snow_light"
    flurries = "flurries"
    tstorm = "tstorm"
    rain_heavy = "rain_heavy"
    rain = "rain"
    rain_light = "rain_light"
    drizzle = "drizzle"
    fog_light = "fog_light"
    fog = "fog"
    cloudy = "cloudy"
    mostly_cloudy = "mostly_cloudy"
    partly_cloudy = "partly_cloudy"
    mostly_clear = "mostly_clear"
    clear = "clear"


class observation(BaseModel):
    precipitation: Optional[float] = None
    precipitation_type: Optional[str] = None
    weather_code: weather_codes
    temp: float
    visibility: float
    cloud_cover: float
    cloud_base: Optional[float] = None
    cloud_ceiling: Optional[float] = None
    observation_time: datetime


class weather_forecast(BaseModel):
    current_conditions: observation
    future_conditions: observation

    def snowing(self) -> bool:
        its_snowing = False

        if (
            self.current_conditions.weather_code in self._snowing_weather_codes
            and self.current_conditions.precipitation > 0.1
        ) or (
            self.future_conditions.weather_code in self._snowing_weather_codes
            and self.future_conditions.precipitation > 0.1
        ):
            its_snowing = True

        return its_snowing

    _snowing_weather_codes = [
        "freezing_rain_heavy",
        "freezing_rain",
        "freezing_rain_light",
        "freezing_drizzle",
        "ice_pellets_heavy",
        "ice_pellets",
        "ice_pellets_light",
        "snow_heavy",
        "snow",
        "snow_light",
        "flurries",
    ]
