from fastapi import FastAPI
import uvicorn
import json
import logging
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from cava.webhook.publisher import Publisher
import os
from cava.models.amcrest import event as amcrest_motion

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s: %(levelname)s: %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s: %(levelname)s: %(message)s"
log_config["formatters"]["access"]["datefmt"] = "%m/%d/%Y %I:%M:%S %p"
log_config["formatters"]["default"]["datefmt"] = "%m/%d/%Y %I:%M:%S %p"

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)

# Declare our application
app = FastAPI(
    description="A Simple API for accepting events from the SniderPad",
    version="0.0.1",
    title="Cava",
)

# Configuration parameters for RabbitMQ
config = {
    "exchangeName": "message_exchange",
    "userName": "cava",
    "password": os.getenv("CAVA_PASS"),
    "host": os.getenv("RABBITMQ_SERVICE_SERVICE_HOST"),
    "port": "5672",
    "virtualHost": "/",
}

# Get a connection to RabbitMQ
publisher = Publisher(config)


@app.put("/api/v01/motion")
async def motion(motion: amcrest_motion):
    """
    Accepts
    """
    logging.info(f"Received motion from {motion.camera}")
    str_obj = motion.json()
    publisher.publish(str_obj, "motion")


if __name__ == "__main__":
    uvicorn.run(app, log_config=log_config, host="0.0.0.0", port=8000)
