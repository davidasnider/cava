import requests
from pydantic import BaseModel, HttpUrl
from typing import Union, List, Optional
from requests.auth import HTTPDigestAuth
import statsd
import cava
from cava.models.settings import Settings


log = cava.log()
settings = Settings()


# This will let us execute an action against indigo
class indigo_executor(BaseModel):
    uri: str
    success: bool = False
    host: HttpUrl = settings.INDIGO_URL
    user: str = settings.INDIGO_USER
    password: str = settings.INDIGO_PASS.get_secret_value()

    @property
    def url(self):
        return f"{self.host}{self.uri}"

    # Run the activity specified
    def execute_action(self):
        print("User: ", self.user)
        r = requests.request(
            "EXECUTE", self.url, auth=HTTPDigestAuth(self.user, self.password)
        )
        if r.ok:
            self.success = True
        log.info(f"executing indigo action {self.url}")


# This will send a metric to Influxdb
class influxdb_executor(BaseModel):
    metric_name: str
    metric: Union[int, float]
    tags: Optional[str] = None
    host: str = "metrics.thesniderpad.com"
    port: str = "8125"

    # Run the activity specified
    def execute_action(self):
        statsd_connection = statsd.StatsClient(self.host, self.port)
        influxdb_measure = f"{self.metric_name}"
        if self.tags is not None:
            influxdb_measure = influxdb_measure + ",{self.tags}"
        statsd_connection.gauge(influxdb_measure, self.metric)
        log.info(f"logging metric {influxdb_measure} with value {self.metric}")


# This maps a rule to an action executor
class action(BaseModel):
    name: str  # What do we name this? weather_to_metrics
    action: str  # what is the actions tring we'll see from correlator?

    # Something that does a thing... Must have an execute_action function
    executor: Union[indigo_executor, influxdb_executor]


class actions(BaseModel):
    action_list: Optional[List[action]] = []  # An iterable list of actions to run

    def run_actions(self, found_action: str):
        for action in self.action_list:
            if action.action == found_action:
                action.executor.execute_action()
