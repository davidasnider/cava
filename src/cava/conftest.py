import pytest
import os
import time
import pika


@pytest.fixture
def amcrest_json():
    valid_json = {"code": "one", "action": "one", "index": 1, "camera": "one"}
    return valid_json


@pytest.fixture
def weather_json():
    valid_json = {
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
    return valid_json


# Setup a session level monkeypatch object
@pytest.fixture(scope="session")
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch

    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session")
def set_environ(monkeypatch_session):
    monkeypatch_session.setenv("RABBITMQ_DEFAULT_USER", "test-user")
    monkeypatch_session.setenv("RABBITMQ_DEFAULT_PASS", "test-password")
    monkeypatch_session.setenv("RABBITMQ_SERVICE_SERVICE_HOST", "localhost")
    monkeypatch_session.setenv("CAVA_URL", "http://localhost:8000")
    monkeypatch_session.setenv("CAVA_URI", "/api/v01/motion")
    monkeypatch_session.setenv("CAVA_CAMERA", "some-test-camera")
    monkeypatch_session.setenv("CAVA_USER", "test-user")
    monkeypatch_session.setenv("CAVA_PASSWORD", "test-passwerd")
    monkeypatch_session.setenv("CLIMACELL_API_KEY", "test-api-key")
    monkeypatch_session.setenv("TZ", "America/Denver")


@pytest.fixture(scope="session")
def setup_module(set_environ):
    command = "docker run -d --name rabbitmq-management --rm -p 5672:5672 -p 8080:15672 -e RABBITMQ_DEFAULT_USER -e RABBITMQ_DEFAULT_PASS rabbitmq:3.8.9-management"
    os.system(command)  # nosec (it's for a test)
    timeout = 60
    default_user = os.getenv("RABBITMQ_DEFAULT_USER")
    print(f"RABBITMQ_DEFAULT_USER = {default_user}")

    userName = os.getenv("RABBITMQ_DEFAULT_USER")
    password = os.getenv("RABBITMQ_DEFAULT_PASS")
    credentials = pika.PlainCredentials(userName, password)
    parameters = pika.ConnectionParameters(
        "localhost",
        "5672",
        "/",
        credentials,
    )

    # Wait for rabbit
    start_time = time.perf_counter()
    while True:
        try:
            with pika.BlockingConnection(parameters):
                break
        except pika.exceptions.IncompatibleProtocolError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError("Waited too long for rabbimtq") from ex
    yield

    command = "docker stop rabbitmq-management"
    os.system(command)  # nosec using in a test
