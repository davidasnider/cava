from fastapi import FastAPI
import uvicorn
import json
import logging
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from publisher import Publisher
import os

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


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


# Schema for our motion endpoint
class Motion(BaseModel):
    device: str = Field(
        ..., title="Device name", min_length=1, description="Device detecting motion"
    )

    class Config:
        schema_extra = {"example": {"device": "driveway-cam"}}


@app.put("/api/v01/motion")
async def motion(motion: Motion):
    """
    Accepts
    """
    str_obj = json.dumps(jsonable_encoder(motion))
    publisher.publish(str_obj, "motion")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
