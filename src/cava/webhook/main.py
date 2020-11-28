from fastapi import FastAPI
import uvicorn
from cava.webhook.publisher import Publisher
import os
from cava.models.amcrest import event as amcrest_motion
from cava.models.climacell import weather_forecast as weather
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


@app.put("/api/v01/weather")
async def weather(weather: weather):
    """
    See model definition for fields
    """
    log.info("Received weather forecast")
    str_obj = weather.json()
    log.debug(f"Weather object received: {weather}")
    publisher.publish(str_obj, "weather")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=cava.log_config())
