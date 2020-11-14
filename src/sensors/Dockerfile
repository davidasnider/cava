# Build Image
FROM python:3.8 AS compile-image

RUN useradd -m -u 1000 sensor
USER sensor
COPY requirements.txt .
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
ADD amcrest_motion.py /app/amcrest_motion.py

CMD ["python3", "amcrest_motion.py"]
