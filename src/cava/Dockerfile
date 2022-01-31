# Build Image
FROM python:3.9 AS compile-image

RUN useradd -m -u 1000 cava
USER cava
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime Image
FROM python:3.9-slim AS final-image
RUN useradd -m -u 1000 cava
USER cava
COPY --from=compile-image /home/cava/.local /home/cava/.local

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/cava/.local/bin:$PATH

WORKDIR /app
ADD . /app/cava
ADD logger_config.yaml /app/cava/logger_config.yaml

CMD ["python3", "-m", "cava.sensors.weather.tomorrow_io"]
