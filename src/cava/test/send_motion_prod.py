"""
This simulates a motion detection event against the prod system.

Run using the following command:

cd ~/code/cava/src
python3 -m cava.test.send_motion_prod
"""

from cava.models.amcrest import event as amcrest_motion
import requests

url = "http://cava.thesniderpad.com:8000"
uri = "/api/v01/motion"
my_motion = amcrest_motion()

my_motion.code = "VideoMotion"
my_motion.action = "Start"
my_motion.index = 0
my_motion.camera = "Test Camera"

result = requests.put(url + uri, my_motion.json())

print(result)
