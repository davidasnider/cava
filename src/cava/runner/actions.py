# from cava.models.actions import executor, action
import requests


# This will let us execute an action against indigo
class indigo_executor:
    def __init__(self, uri):
        self.uri = uri  # This should have the starting /
        self.success = False  # By default assume we fail to run our action
        self.host = "http://blanc:8000"
        self.url = f"{self.host}{uri}"

    # Run the activity specified
    def execute_action(self):
        r = requests.request("EXECUTE", self.url)
        if r.ok:
            self.success = True
