from fastapi import FastAPI
import uvicorn
import json
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from cava.webhook.publisher import Publisher
import os
from cava.models.amcrest import event as amcrest_motion
import cava

log = cava.log()

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

log.debug(f"RabbitMQ Config: {config}")

# Get a connection to RabbitMQ
publisher = Publisher(config)


@app.put("/api/v01/motion")
async def motion(motion: amcrest_motion):
    """
    Accepts
    """
    log.info(f"Received motion from {motion.camera}")
    str_obj = motion.json()
    log.debug(f"motion object received: {motion}")
    publisher.publish(str_obj, "motion")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=cava.log_config())
