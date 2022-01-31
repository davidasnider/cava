# Build Image
FROM python:3.9 AS compile-image

RUN useradd -m -u 1000 sensor
USER sensor
COPY sensors/weather/requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime Image
FROM python:3.8-slim AS final-image
RUN useradd -m -u 1000 sensor
USER sensor
COPY --from=compile-image /home/sensor/.local /home/sensor/.local

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/sensor/.local/bin:$PATH

WORKDIR /app
ADD sensors/weather /app/cava/sensors/weather
ADD models /app/cava/models
ADD __init__.py /app/cava/__init__.py
ADD logger_config.yaml /app/cava/logger_config.yaml

CMD ["python3", "-m", "cava.sensors.weather.climacell"]
