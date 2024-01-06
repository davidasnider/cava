import cava
from cava.messages.receiver import Receiver
import time
import cava.runner.my_actions as my_actions

log = cava.log()


def callback(ch, method, properties, body):
    log.debug(f"Received {body} on routing_key {method.routing_key}")
    log.info(f"executing action {body.decode()}")
    # ack the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
    my_actions.rules_to_actions.run_actions(body.decode())


def main():
    # We need to listen for actions coming from rabbitmq
    receiver = Receiver("run.*", queue_name="actions")

    # Connect to rabbitmq and associate the callback function
    retries = 0
    while retries < 5:
        try:
            receiver.connect()
        except Exception as e:
            log.info("rabbitmq connection failed, retry in 5 seconds")
            log.debug(f"exception is {e}")
            time.sleep(5)
            retries += 1
        else:
            break

    if retries == 5:
        log.info("Unable to connect to rabbitmq, quitting")
        exit()

    receiver.consume(callback)


if __name__ == "__main__":
    main()
