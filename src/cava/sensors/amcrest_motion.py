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


def convert_to_dict(kv_list):
    return {item.split("=")[0]: item.split("=")[1] for item in kv_list}


for event in camera.event_stream("VideoMotion"):
    event = event.rstrip().strip()  # Get rid of carriage returns
    parsed_event = event.split(";")
    dict_event = convert_to_dict(parsed_event)
    dict_event["camera"] = mycamera
    my_event = amcrest_event(**dict_event)
    log.info(f"{my_event}")

    result = requests.put(str(url) + uri, my_event.model_dump_json())
