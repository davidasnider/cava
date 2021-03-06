# Build Image
FROM python:3.8 AS compile-image

RUN useradd -m -u 1000 webhook
USER webhook
COPY webhook/requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime Image
FROM python:3.8-slim AS final-image
RUN useradd -m -u 1000 webhook
USER webhook
COPY --from=compile-image /home/webhook/.local /home/webhook/.local

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/webhook/.local/bin:$PATH

WORKDIR /app
ADD webhook /app/cava/webhook
ADD messages /app/cava/messages
ADD models /app/cava/models
ADD logger_config.yaml /app/cava
ADD __init__.py /app/cava

CMD ["uvicorn", "--host", "0.0.0.0", "cava.webhook.main:app", "--log-config", "/app/cava/logger_config.yaml"]
