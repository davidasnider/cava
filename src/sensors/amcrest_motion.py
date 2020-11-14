from amcrest import AmcrestCamera
import requests
import json
import os

url = os.getenv("CAVA_URL")
uri = os.getenv("CAVA_URI")
camera = os.getenv("CAVA_CAMERA")
user = os.getenv("CAVA_USER")
password = os.getenv("CAVA_PASSWORD")

camera = AmcrestCamera(camera, 80, user, password).camera
device = camera.machine_name.rstrip()
device = device.split("=")[1]
print(f"Connected to camera {device}")


for event in camera.event_stream("VideoMotion"):
    event = event.rstrip().strip()  # Get rid of carriage returns
    print(event)
    parsed_event = event.split(";")
    if parsed_event[1] == "action=Start":
        data = {"device": device}
        result = requests.put(url + uri, data=json.dumps(data))
