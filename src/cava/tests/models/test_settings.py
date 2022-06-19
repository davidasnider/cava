from cava.models.settings import Settings
import os


# We need to be able to override environment variables that are set in the
# .env file, this is especially important when running many cameras with different
# url's. These will be distributed as kubernetes environment variables, but the
# .env file will also be present, need to ensure values are overriden properly.
def test_override_env_file():
    os.environ["CAVA_CAMERA"] = "some-test-camera"
    settings = Settings()
    assert settings.CAVA_CAMERA == "some-test-camera"
