from pathlib import Path

from pydantic_settings import BaseSettings


_CURRENT_PATH: Path = Path(__file__).parent


class Config(BaseSettings):
    """Configuration class for the API application.

    This class defines all the configuration parameters used throughout the application,
    including paths, connection settings, and feature flags.
    """

    ROOT_PATH: Path = _CURRENT_PATH
    FACES_PATH: Path = ROOT_PATH / "faces"
    VIDEOS_PATH: Path = ROOT_PATH / "videos"

    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    ICE_CANDIDATE_HOST: str | None = None
    ENABLE_HANDLE_STREAM: bool = True


CONFIG = Config()
