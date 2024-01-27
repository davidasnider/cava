from cava.models.tomorrow_io import weather_observation
from cava.models.settings import Settings
from pydantic import ValidationError
import pytest
from unittest.mock import Mock, patch


def test_weather_observation_good(weather_json):
    my_weather_observation = weather_observation(**weather_json)
    assert my_weather_observation.current_conditions.snow_accumulation == 0.0


def test_weather_missing_field(weather_json):
    del weather_json["current_conditions"]["humidity"]

    with pytest.raises(ValidationError):
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


def test_create_from_live_data_success(weather_json):
    # Create a mock for the requests.post method
    with patch("cava.models.tomorrow_io.requests.post") as mock_post:

        # Create a mock for the response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": {
                "timelines": [
                    {
                        "intervals": [
                            {"values": weather_json["current_conditions"]},
                            {"values": weather_json["future_conditions"]},
                        ]
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        # Call the create_from_live_data method
        my_weather_observation = weather_observation.create_from_live_data()

        # Check that the current_conditions and future_conditions are correct
        assert (
            my_weather_observation.current_conditions
            == weather_observation(**weather_json).current_conditions
        )
        assert (
            my_weather_observation.future_conditions
            == weather_observation(**weather_json).future_conditions
        )


def test_create_from_live_data_too_many_requests(weather_json):
    # Create a mock for the requests.post method
    with patch("cava.models.tomorrow_io.requests.post") as mock_post, patch(
        "cava.models.tomorrow_io.time.sleep"
    ) as mock_sleep:

        # Create a mock for the response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "5"}
        mock_post.return_value = mock_response

        # Call the create_from_live_data method and check that it raises an exception
        with pytest.raises(Exception):
            weather_observation.create_from_live_data()

        # Check that the sleep method was called
        assert mock_sleep.called


def test_create_from_live_data_other_error(weather_json):
    # Create a mock for the requests.post method
    with patch("cava.models.tomorrow_io.requests.post") as mock_post, patch(
        "cava.models.tomorrow_io.time.sleep"
    ) as mock_sleep:

        # Create a mock for the response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Call the create_from_live_data method and check that it raises an exception
        with pytest.raises(Exception):
            weather_observation.create_from_live_data()

        # Check that the sleep method was called
        assert mock_sleep.called


def test_log_observation(weather_json):
    # Create a mock for the log.info method
    with patch("cava.models.tomorrow_io.log.info") as mock_info:

        # Create an instance of the weather_observation class
        my_weather_observation = weather_observation(**weather_json)

        # Call the log_observation method
        my_weather_observation.log_observation()

        # Check that the info method was called with the correct parameters
        mock_info.assert_any_call(
            f"Current conditions: {my_weather_observation.current_conditions}"
        )
        mock_info.assert_any_call(
            f"Future conditions: {my_weather_observation.future_conditions}"
        )


def test_publish_to_cava_success(weather_json):
    # Get settingsd
    settings = Settings()

    # Create a mock for the requests.put method
    with patch("cava.models.tomorrow_io.requests.put") as mock_put, patch(
        "cava.models.tomorrow_io.log.info"
    ) as mock_info:

        # Create a mock for the response
        mock_response = Mock()
        mock_response.ok = True
        mock_put.return_value = mock_response

        # Create an instance of the weather_observation class
        my_weather_observation = weather_observation(**weather_json)

        # Call the publish_to_cava method
        my_weather_observation.publish_to_cava()

        # Check that the put method was called with the correct parameters
        mock_put.assert_called_once_with(
            str(settings.CAVA_URL) + "api/v01/weather",
            data=my_weather_observation.model_dump_json(by_alias=True),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        # Check that the info method was called with the correct parameters
        mock_info.assert_called_once_with("Published weather observation to CAVA")


def test_publish_to_cava_failure(weather_json):
    # Get settings
    settings = Settings()

    # Create a mock for the requests.put method
    with patch("cava.models.tomorrow_io.requests.put") as mock_put, patch(
        "cava.models.tomorrow_io.log.error"
    ) as mock_error:

        # Create a mock for the response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_put.return_value = mock_response

        # Create an instance of the weather_observation class
        my_weather_observation = weather_observation(**weather_json)

        # Call the publish_to_cava method
        my_weather_observation.publish_to_cava()

        # Check that the put method was called with the correct parameters
        mock_put.assert_called_once_with(
            str(settings.CAVA_URL) + "api/v01/weather",
            data=my_weather_observation.model_dump_json(by_alias=True),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        # Check that the error method was called with the correct parameters
        mock_error.assert_called_once_with(
            f"Failed to publish weather observation to CAVA, error code: {mock_response.status_code}"
        )
