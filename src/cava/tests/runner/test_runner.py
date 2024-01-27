from cava.runner.actions import indigo_executor
from unittest.mock import patch, Mock
from pydantic import HttpUrl
from requests.models import Response
from cava.models.settings import Settings
import pytest
import json


@pytest.mark.integration
def test_call_action_group():
    action_group_id = 635158869
    my_executor = indigo_executor(action_group_id=action_group_id)
    my_executor.execute_action()
    assert my_executor.success  # This should be true


@pytest.mark.integration
def test_call_action_group_fail():
    action_group_id = 123456789
    my_executor = indigo_executor(action_group_id=action_group_id)
    my_executor.execute_action()
    assert my_executor.success is False  # This should be true


def test_url_property():
    executor = indigo_executor(
        action_group_id=1, host=HttpUrl(url="http://localhost:8000/")
    )
    assert executor.url == "http://localhost:8000/v2/api/command"


@patch("requests.post")
def test_execute_action(mock_post):
    mock_response = Response()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    executor = indigo_executor(
        action_group_id=1, host=HttpUrl(url="http://localhost:8000/")
    )
    executor.execute_action()

    assert executor.success is True
    mock_post.assert_called_once()


@patch("requests.post")
def test_execute_action_success(mock_post):
    # Get settings
    settings = Settings()

    # Create a mock for the response
    mock_response = Mock()
    mock_response.ok = True
    mock_post.return_value = mock_response

    # Create an instance of the indigo_executor class
    my_executor = indigo_executor(
        action_group_id=1, host=HttpUrl(url="http://localhost:8000/")
    )

    # Call the execute_action method
    my_executor.execute_action()

    # Check that the post method was called with the correct parameters
    execute_action_group_message = {
        "message": "indigo.actionGroup.execute",
        "objectId": my_executor.action_group_id,
    }
    headers = {"Authorization": f"Bearer {settings.indigo_api_key.get_secret_value()}"}
    mock_post.assert_called_once_with(
        my_executor.url, headers=headers, data=json.dumps(execute_action_group_message)
    )

    # Check that the success attribute is True
    assert my_executor.success is True


@patch("requests.post")
def test_execute_action_failure(mock_post):
    settings = Settings()
    # Create a mock for the response
    mock_response = Mock()
    mock_response.ok = False
    mock_post.return_value = mock_response

    # Create an instance of the indigo_executor class
    my_executor = indigo_executor(
        action_group_id=1, host=HttpUrl(url="http://localhost:8000/")
    )

    # Call the execute_action method
    my_executor.execute_action()

    # Check that the post method was called with the correct parameters
    execute_action_group_message = {
        "message": "indigo.actionGroup.execute",
        "objectId": my_executor.action_group_id,
    }
    headers = {"Authorization": f"Bearer {settings.indigo_api_key.get_secret_value()}"}
    mock_post.assert_called_once_with(
        my_executor.url, headers=headers, data=json.dumps(execute_action_group_message)
    )

    # Check that the success attribute is False
    assert my_executor.success is False
