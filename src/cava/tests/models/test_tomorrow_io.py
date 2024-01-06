from cava.models.tomorrow_io import weather_observation
import pytest
import pydantic


def test_weather_observation_good(weather_json):
    my_weather_observation = weather_observation(**weather_json)
    assert my_weather_observation.current_conditions.snow_accumulation == 0.0


def test_weather_missing_field(weather_json):
    del weather_json["current_conditions"]["humidity"]

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        weather_observation(**weather_json)


def test_is_snowing_current_conditions(weather_json):
    weather_json["current_conditions"]["preciptiationType"] = 2  # 2 = Snow
    weather_json["current_conditions"]["snowIntensity"] = 1.5

    snowing_forecast = weather_observation(**weather_json)
    assert snowing_forecast.snowing is True


def test_is_snowing_future_conditions(weather_json):
    weather_json["future_conditions"]["precipitationType"] = 2  # 2 = Snow
    weather_json["future_conditions"]["snowAccumulation"] = 1.5

    snowing_forecast = weather_observation(**weather_json)
    assert snowing_forecast.snowing is True


def test_is_not_snowing(weather_json):
    snowing_forecast = weather_observation(**weather_json)
    assert snowing_forecast.snowing is False
