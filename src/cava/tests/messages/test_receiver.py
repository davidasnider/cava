from cava.messages.receiver import Receiver
from cava.messages.publisher import Publisher


def test_receiver_init():
    my_receiver = Receiver()
    assert my_receiver._config["userName"] == "guest"


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
