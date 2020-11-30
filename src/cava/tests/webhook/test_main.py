"""
Let's test out some functions
"""

from fastapi.testclient import TestClient
import json


def test_write_weather(weather_json, set_environ):
    from cava.webhook.main import app  # Import here to get environment vars

    client = TestClient(app)
    response = client.put("/api/v01/weather", data=json.dumps(weather_json))
    assert response.status_code == 200  # nosec


def test_write_motion(amcrest_json, set_environ):
    from cava.webhook.main import app  # Import here to get environment vars

    client = TestClient(app)
    response = client.put("/api/v01/motion", data=json.dumps(amcrest_json))
    assert response.status_code == 200  # nosec
