from cava.models.amcrest import event as amcrest_motion
import requests
import time

url = "http://localhost:8000"
uri = "/api/v01/motion"
my_motion = amcrest_motion()

my_motion.code = "VideoMotion"
my_motion.action = "Start"
my_motion.index = 0
my_motion.camera = "Test Camera"

while True:
    result = requests.put(url + uri, my_motion.json())
    time.sleep(1)

print(result)
