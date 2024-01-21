# FILEPATH: /Users/david/code/cava/tests/test_init.py

from cava import log_config


def test_log_config():
    config = log_config()
    assert isinstance(config, dict)  # Check that it returns a dictionary

    assert "handlers" in config
    assert "formatters" in config
    assert "loggers" in config
    assert "cava" in config["loggers"]
    assert "level" in config["loggers"]["cava"]
    assert config["loggers"]["cava"]["level"] == "INFO"
