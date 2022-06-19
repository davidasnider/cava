import pytest
import os
import time
import pika
import subprocess
from cava.models.settings import Settings

settings = Settings()


@pytest.fixture
def amcrest_json():
    valid_json = {"code": "one", "action": "one", "index": 1, "camera": "one"}
    return valid_json


@pytest.fixture
def weather_json():
    valid_json = {
        "current_conditions": {
            "temperature": "20.0",
            "humidity": "50.0",
            "snowIntensity": "0.0",
            "precipitationType": "Snow",
            "snowAccumulation": "0.0",
        },
        "future_conditions": {
            "temperature": "20.0",
            "humidity": "50.0",
            "snowIntensity": "0.0",
            "precipitationType": "Snow",
            "snowAccumulation": "0.0",
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


# @pytest.fixture(scope="session")
# def set_environ(monkeypatch_session):
#     # First grab from the .env file if it exists

#     print(os.getenv("INDIGO_USER"))

#     # Now overwrite stuff for testing
#     monkeypatch_session.setenv("RABBITMQ_DEFAULT_USER", "guest")
#     monkeypatch_session.setenv("RABBITMQ_DEFAULT_PASS", "guest")
#     monkeypatch_session.setenv("RABBITMQ_SERVICE_SERVICE_HOST", "localhost")
#     monkeypatch_session.setenv("CAVA_URL", "http://localhost:8000")
#     monkeypatch_session.setenv("CAVA_URI", "/api/v01/motion")
#     monkeypatch_session.setenv("CAVA_CAMERA", "some-test-camera")
#     monkeypatch_session.setenv("CAVA_USER", "test-user")
#     monkeypatch_session.setenv("CAVA_PASSWORD", "test-passwerd")
#     monkeypatch_session.setenv("TOMORROW_IO_API_KEY", "test-api-key")
#     monkeypatch_session.setenv("TZ", "America/Denver")
#     monkeypatch_session.setenv(
#         "INDIGO_USER", os.getenv("INDIGO_USER")
#     )  # Weird hack to get this into the test environment
#     monkeypatch_session.setenv(
#         "INDIGO_PASS", os.getenv("INDIGO_PASS")
#     )  # Weird hack to get this into the test environment


@pytest.fixture(scope="session")
def setup_module():
    # Check if container is still running
    subprocess_return = subprocess.run(
        ["lima", "nerdctl", "ps", "-a", "-q"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    if subprocess_return:
        # Apparently the container is still running, manually delete it
        subprocess_return = subprocess.run(
            ["lima", "nerdctl", "rm", "-f", "rabbitmq-management"],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")

    command = "lima nerdctl run -d --name rabbitmq-management -p 5672:5672 -p 8080:15672 rabbitmq:3.8.9-management"
    os.system(command)  # nosec (it's for a test)
    timeout = 600
    default_user = settings.RABBITMQ_DEFAULT_USER
    print(f"RABBITMQ_DEFAULT_USER = {default_user}")

    userName = settings.RABBITMQ_DEFAULT_USER
    password = settings.RABBITMQ_DEFAULT_PASS.get_secret_value()
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
        except Exception as ex:
            time.sleep(0.5)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError("Waited too long for rabbimtq") from ex
    yield

    command = "lima nerdctl rm -f rabbitmq-management"
    os.system(command)  # nosec using in a test
