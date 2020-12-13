# Build Image
FROM python:3.8 AS compile-image

RUN useradd -m -u 1000 correlator
USER correlator
COPY correlator/requirements.txt /requirements.txt
RUN pip install --user -r requirements.txt

# Runtime Image
FROM python:3.8-slim AS final-image
RUN useradd -m -u 1000 correlator
USER correlator
COPY --from=compile-image /home/correlator/.local /home/correlator/.local

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/correlator/.local/bin:$PATH

WORKDIR /app
COPY correlator /app/cava/correlator
COPY messages /app/cava/messages
COPY models /app/cava/models
COPY __init__.py /app/cava/__init__.py
COPY logger_config.yaml /app/cava/logger_config.yaml

CMD ["python3", "-m", "cava.correlator.main"]
