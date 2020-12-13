# Build Image
FROM python:3.8 AS compile-image

RUN useradd -m -u 1000 runner
USER runner
COPY runner/requirements.txt /requirements.txt
RUN pip install --user -r requirements.txt

# Runtime Image
FROM python:3.8-slim AS final-image
RUN useradd -m -u 1000 runner
USER runner
COPY --from=compile-image /home/runner/.local /home/runner/.local

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/runner/.local/bin:$PATH

WORKDIR /app
COPY runner /app/cava/runner
COPY messages /app/cava/messages
# COPY models /app/cava/models
COPY __init__.py /app/cava/__init__.py
COPY logger_config.yaml /app/cava/logger_config.yaml

CMD ["python3", "-m", "cava.runner.main"]
