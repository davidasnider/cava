from cava.models.climacell import weather_forecast
import pytest
import pydantic


def test_weather_forecast_good(weather_json):

    my_weather_forecast = weather_forecast(**weather_json)
    assert my_weather_forecast.current_conditions.precipitation == 0.0


def test_weather_forecast_bad_weather_code(weather_json):
    weather_json["current_conditions"]["weather_code"] = "Not a valid weather code"

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        weather_forecast(**weather_json)


def test_weather_missing_field(weather_json):
    del weather_json["current_conditions"]["weather_code"]

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        weather_forecast(**weather_json)


def test_is_snowing_current_conditions(weather_json):
    weather_json["current_conditions"]["weather_code"] = "snow"
    weather_json["current_conditions"]["precipitation"] = 0.2

    snowing_forecast = weather_forecast(**weather_json)
    assert snowing_forecast.snowing is True


def test_is_snowing_future_conditions(weather_json):
    weather_json["future_conditions"]["weather_code"] = "snow"
    weather_json["future_conditions"]["precipitation"] = 0.2

    snowing_forecast = weather_forecast(**weather_json)
    assert snowing_forecast.snowing is True


def test_is_not_snowing(weather_json):

    snowing_forecast = weather_forecast(**weather_json)
    assert snowing_forecast.snowing is False


def test_climacell_ttl_return_int(weather_json):
    my_weather_forecast = weather_forecast(**weather_json)
    assert int(my_weather_forecast.ttl())
