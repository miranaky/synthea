from dataclasses import dataclass
from pydantic import BaseSettings


def conf():
    """
    load configuration
    return
    """

    return Config()


class Settings(BaseSettings):
    DB_URL: str


settings = Settings()


@dataclass
class Config:
    """Basic configuration"""

    DB_URL: str = settings.DB_URL
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
