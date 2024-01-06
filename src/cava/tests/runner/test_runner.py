from cava.runner.actions import indigo_executor
from unittest.mock import patch
from pydantic import HttpUrl
from requests.models import Response


def test_call_action_group():
    action_group_id = 635158869
    my_executor = indigo_executor(action_group_id=action_group_id)
    my_executor.execute_action()
    assert my_executor.success  # This should be true


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
