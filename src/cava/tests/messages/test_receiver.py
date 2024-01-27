from cava.messages.receiver import Receiver
from cava.messages.publisher import Publisher
import pytest
from unittest.mock import patch, Mock


@pytest.mark.integration
def test_receiver_init():
    my_receiver = Receiver()
    assert my_receiver._config["userName"] == "guest"


@pytest.mark.integration
def test_receive_message():
    test_message = "test message"
    my_receiver = Receiver(routingKey="pytest")
    my_receiver.connect()
    my_publisher = Publisher()
    my_publisher.publish(test_message, routingKey="pytest")
    for method, properties, body in my_receiver.channel.consume(
        my_receiver.queue_name, auto_ack=True, inactivity_timeout=5
    ):
        print(body)
        message = body.decode()
        break
    my_receiver.channel.cancel()
    assert message == test_message


def test_connect_with_queue_name():
    # Create a mock for the pika.PlainCredentials and pika.ConnectionParameters classes
    with patch(
        "cava.messages.receiver.pika.BlockingConnection"
    ) as mock_blocking_connection:
        # Create a mock for the channel
        mock_channel = Mock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        # Create an instance of the Receiver class with a queue name
        my_receiver = Receiver(queue_name="test_queue")

        # Call the connect method
        my_receiver.connect()

        # Check that the queue_declare method was called with the correct parameters
        mock_channel.queue_declare.assert_called_once_with("test_queue")

        # Check that the queue_bind method was called with the correct parameters
        mock_channel.queue_bind.assert_called_once_with(
            exchange=my_receiver._config["exchangeName"],
            queue="test_queue",
            routing_key=my_receiver.routingKey,
        )


def test_consume():
    # Create a mock for the pika.BlockingConnection class
    with patch(
        "cava.messages.receiver.pika.BlockingConnection"
    ) as mock_blocking_connection:

        # Create a mock for the channel
        mock_channel = Mock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        # Create an instance of the Receiver class
        my_receiver = Receiver()

        # Call the connect method
        my_receiver.connect()

        # Create a mock for the callback
        mock_callback = Mock()

        # Call the consume method
        my_receiver.consume(mock_callback)

        # Check that the basic_consume method was called with the correct parameters
        mock_channel.basic_consume.assert_called_once_with(
            queue=my_receiver.queue_name, on_message_callback=mock_callback
        )

        # Check that the start_consuming method was called
        mock_channel.start_consuming.assert_called_once()
