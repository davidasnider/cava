from cava.messages.publisher import Publisher
import pytest


def test_publish_init(set_environ):
    my_publisher = Publisher()
    assert my_publisher._config["userName"] == "guest"


def test_publish_init_missing_env(setup_module, monkeypatch):
    monkeypatch.delenv("RABBITMQ_DEFAULT_USER")

    with pytest.raises(SystemExit):
        Publisher()


def test_publish_message(set_environ):
    my_publisher = Publisher()
    my_publisher.publish("test message")  # If this fails, test fails
