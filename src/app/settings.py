import enum
from http import HTTPMethod
from typing import Literal
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingLevel(enum.StrEnum):
    DEBUG = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()
    CRITICAL = enum.auto()


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="app_")

    cors_allow_origins: list[str] = []
    cors_allow_methods: list[Literal["*"] | HTTPMethod] = ["*"]
    cors_allow_headers: list[str] = ["authorization"]

    image_path: str = "images"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    driver: str = "postgresql+asyncpg"
    name: str
    username: str
    password: str
    host: str

    echo: bool = False

    @property
    def url(self) -> str:
        password = quote_plus(self.password)
        return f"{self.driver}://{self.username}:{password}@{self.host}/{self.name}"


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="logging_")

    level: LoggingLevel = LoggingLevel.INFO


class TelegramBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="tg_")

    name: str
    url: str
    token: str
    time_limit: int = 1
    rate_limit: int = 30
