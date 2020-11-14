# Build Image
FROM python:3.8-slim AS compile-image
RUN useradd -m -u 1000 metrics
USER metrics
COPY requirements.txt .
RUN pip install --user -r requirements.txt && \
    pip install --user ptvsd

# Runtime Image again
FROM python:3.8-slim AS build-image

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN useradd -m -u 1000 metrics
USER metrics
# Add .local/bin to the path
ENV PATH /home/metrics/.local/bin:$PATH
COPY --from=compile-image /home/metrics/.local /home/metrics/.local
WORKDIR /app
ADD metrics_pusher.py /app/metrics_pusher.py

CMD ["python", "-m", "ptvsd", "--port", "3000", "--host", "0.0.0.0", "metrics_pusher.py"]
