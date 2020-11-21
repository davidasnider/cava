from amcrest import AmcrestCamera
import requests
import json
import os
import logging

from cava.models.amcrest import event as amcrest_event


# Setup logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

url = os.getenv("CAVA_URL")
uri = os.getenv("CAVA_URI")
mycamera = os.getenv("CAVA_CAMERA")
user = os.getenv("CAVA_USER")
password = os.getenv("CAVA_PASSWORD")

logging.info("Starting Amcrest Sensor")
camera = AmcrestCamera(mycamera, 80, user, password).camera
logging.info(f"Attempting to connect to camera {mycamera}")
device = camera.machine_name.rstrip()
device = device.split("=")[1]
logging.info(f"Connected to {device} on {mycamera}")


for event in camera.event_stream("VideoMotion"):
    event = event.rstrip().strip()  # Get rid of carriage returns
    parsed_event = event.split(";")
    my_event = amcrest_event()
    my_event.camera = mycamera
    for item in parsed_event:
        element = item.split("=")
        if element[0].lower() == "code":
            my_event.code = element[1]
        if element[0].lower() == "action":
            my_event.action = element[1]
        if element[0].lower() == "index":
            my_event.index = element[1]
    logging.info(f"{my_event}")

    result = requests.put(url + uri, my_event.json())
