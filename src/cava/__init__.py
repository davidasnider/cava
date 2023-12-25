import yaml
import logging.config
import pathlib

LOGGING_CONFIG = pathlib.Path(__file__).parent / "logger_config.yaml"

with open(LOGGING_CONFIG) as f:
    config_dict = yaml.safe_load(f)
    logging.config.dictConfig(config_dict)


# get root logger
def log():
    return logging.getLogger(__name__)
    # the __name__ resolve to "main" since we are at the root of the project
    # This will get the root logger since no logger in the configuration has this name.


def log_config():
    return config_dict
