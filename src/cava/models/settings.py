from pydantic import BaseSettings, SecretStr
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """
    Settings for the application.

    Read from the .env file stored in the base directory. For deployments
    the deployment tool will need to create this file.
    """

    # Configures environment variables for the aplication

    CAVA_URL: AnyHttpUrl  # "http://localhost:8000"
    CAVA_URI: str  # "/api/v01/motion"
    CAVA_CAMERA: str  # "bedroom-cam.thesniderpad.com"
    CAVA_USER: str  # "admin"
    CAVA_PASSWORD: SecretStr  # Will not show in logs by default
    RABBITMQ_SERVICE_SERVICE_HOST: str  # "127.0.0.1"
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: SecretStr
    TZ: str  # "America/Denver"
    INDIGO_USER: str  #
    INDIGO_PASS: SecretStr  # Will not show in logs by default
    INDIGO_URL: AnyHttpUrl  # URL of our Indigo API
    TOMORROW_IO_API_KEY: SecretStr
    TOMORROW_IO_LATITUDE: float
    TOMORROW_IO_LONGITUDE: float

    class Config:
        # Read everything from .env
        env_file = ".env"
        env_file_encoding = "utf-8"