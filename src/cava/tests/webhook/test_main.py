"""
Let's test out some functions
"""

from fastapi.testclient import TestClient
import json
import pytest


@pytest.mark.integration
def test_write_weather(weather_json):
    from cava.webhook.main import app  # Import here to get environment vars

    client = TestClient(app)
    response = client.put("/api/v01/weather", content=json.dumps(weather_json))
    assert response.status_code == 200  # nosec


@pytest.mark.integration
def test_write_motion(amcrest_json):
    from cava.webhook.main import app  # Import here to get environment vars

    client = TestClient(app)
    response = client.put("/api/v01/motion", content=json.dumps(amcrest_json))
    assert response.status_code == 200  # nosec
