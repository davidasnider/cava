from cava.messages.publisher import Publisher
import pytest


def test_publish_init():
    my_publisher = Publisher()
    assert my_publisher._config["userName"] == "guest"


@pytest.mark.integration
def test_publish_message():
    my_publisher = Publisher()
    my_publisher.publish("test message")  # If this fails, it will raise an exception
