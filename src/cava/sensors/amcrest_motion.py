from amcrest import AmcrestCamera
import requests
import cava

from cava.models.amcrest import event as amcrest_event
from cava.models.settings import Settings

settings = Settings()

# Setup logging
log = cava.log()

url = settings.CAVA_URL
uri = settings.CAVA_URI
mycamera = settings.CAVA_CAMERA
user = settings.CAVA_USER
password = settings.CAMERA_PASS.get_secret_value()

log.info("Starting Amcrest Sensor")
camera = AmcrestCamera(mycamera, 80, user, password).camera
log.info(f"Attempting to connect to camera {mycamera}")
device = camera.machine_name.rstrip()
# device = device.split("=")[1]
log.info(f"Connected to {device} on {mycamera}")


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
    log.info(f"{my_event}")

    result = requests.put(url + uri, my_event.json())
