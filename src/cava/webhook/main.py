from fastapi import FastAPI
import uvicorn
import json
import logging
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from cava.webhook.publisher import Publisher
import os
import pathlib
from cava.models.amcrest import event as amcrest_motion

LOGGING_CONFIG = pathlib.Path(__file__).parent.parent / "logging.conf"
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project
# This will get the root logger since no logger in the configuration has this name.

# Declare our application
app = FastAPI(
    description="A Simple API for accepting events from the SniderPad",
    version="0.0.1",
    title="Cava",
)

# Configuration parameters for RabbitMQ
config = {
    "exchangeName": "message_exchange",
    "userName": os.getenv("RABBITMQ_DEFAULT_USER"),
    "password": os.getenv("RABBITMQ_DEFAULT_PASS"),
    "host": os.getenv("RABBITMQ_SERVICE_SERVICE_HOST"),
    "port": "5672",
    "virtualHost": "/",
}

logger.debug(f"RabbitMQ Config: {config}")

# Get a connection to RabbitMQ
publisher = Publisher(config)


@app.put("/api/v01/motion")
async def motion(motion: amcrest_motion):
    """
    Accepts
    """
    logger.info(f"Received motion from {motion.camera}")
    str_obj = motion.json()
    logger.debug(f"motion object received: {motion}")
    publisher.publish(str_obj, "motion")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
