# Build Image
FROM python:3.8-slim AS compile-image

RUN useradd -m -u 1000 reader
USER reader
COPY reader/requirements.txt .
RUN pip install --user -r requirements.txt && \
    pip install --user ptvsd


# Runtime Image
FROM python:3.8-slim AS build-image
RUN useradd -m -u 1000 reader
USER reader
COPY --from=compile-image /home/reader/.local /home/reader/.local

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add .local/bin to the path
ENV PATH /home/reader/.local/bin:$PATH

WORKDIR /app
ADD reader /app/cava/reader

CMD ["python", "-m", "ptvsd", "--port", "3000", "--host", "0.0.0.0", "cava/reader/reader.py"]
