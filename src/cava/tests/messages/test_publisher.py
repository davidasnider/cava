from cava.messages.publisher import Publisher
import pytest
from unittest.mock import patch, Mock


@pytest.mark.integration
def test_publish_init():
    my_publisher = Publisher()
    assert my_publisher._config["userName"] == "guest"


@pytest.mark.integration
def test_publish_message():
    my_publisher = Publisher()
    my_publisher.publish("test message")  # If this fails, it will raise an exception


def test_create_connection():
    # Create a mock for the pika.PlainCredentials and pika.ConnectionParameters classes
    with patch(
        "cava.messages.publisher.pika.PlainCredentials"
    ) as mock_plain_credentials, patch(
        "cava.messages.publisher.pika.ConnectionParameters"
    ) as mock_connection_parameters, patch(
        "cava.messages.publisher.pika.BlockingConnection"
    ) as mock_blocking_connection:
        # Create an instance of the Publisher class
        publisher = Publisher()

        # Call the _create_connection method
        connection = publisher._create_connection()

        # Check that the PlainCredentials class was called with the correct parameters
        mock_plain_credentials.assert_called_once_with(
            publisher._config["userName"], publisher._config["password"]
        )

        # Check that the ConnectionParameters class was called with the correct parameters
        mock_connection_parameters.assert_called_once_with(
            publisher._config["host"],
            publisher._config["port"],
            publisher._config["virtualHost"],
            mock_plain_credentials.return_value,
        )

        # Check that the BlockingConnection class was called with the correct parameters
        mock_blocking_connection.assert_called_once_with(
            mock_connection_parameters.return_value
        )

        # Check that the _create_connection method returns the mock connection
        assert connection == mock_blocking_connection.return_value


def test_publish_exception():
    # Create a mock for the pika.PlainCredentials and pika.ConnectionParameters classes
    with patch(
        "cava.messages.publisher.pika.BlockingConnection"
    ) as mock_blocking_connection:
        # Create a mock for the channel
        mock_channel = Mock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        # Make the channel.basic_publish method raise an exception when called
        mock_channel.basic_publish.side_effect = Exception("Publish error")

        # Create an instance of the Publisher class
        publisher = Publisher()

        # Call the publish method and check that it raises a SystemExit error
        with pytest.raises(Exception) as e:
            publisher.publish("test_message", routingKey="test_routing_key")

        assert e.type == Exception
        assert e.value.args[0] == "Publish error"
