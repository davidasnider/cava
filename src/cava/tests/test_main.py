"""
Let's test out some functions
"""

# import mock
# import pytest
# from pytest_mock import mocker
from fastapi.testclient import TestClient

from webhook.main import app

client = TestClient(app)


def test_write_motion():
    valid_json = '{"device": "driveway-cam"}'
    response = client.put("/api/v01/motion", data=valid_json)
    assert response.status_code == 200


def test_write_fail_main():
    invalid_json = '{"device1": "driveway-cam"}'
    response = client.put("/api/v01/motion", data=invalid_json)
    assert response.status_code == 422


# def test_publisher_publish(mocker):
#     # mocker.patch("publisher.publish")
#     mocker.patch.object(Publisher, "publish")
#     valid_json = '{"device": "driveway-cam"}'

#     client.put("/api/v01/motion", data=valid_json)
#     Publisher.publish.assert_called_once_with(valid_json, "motion")
