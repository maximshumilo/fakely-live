from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent
    FACES_PATH: Path = ROOT_PATH / "faces"
    MODELS_PATH: Path = ROOT_PATH / "models"

    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    WORKER_COUNT: int = 4
    DET_SIZE_W: int = 640
    DET_SIZE_H: int = 640
    DET_THRESH: float = 0.5

CONFIG = Config()