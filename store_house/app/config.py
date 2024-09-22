from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class TestDatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class ModeConfig(BaseModel):
    mode: Literal["DEV", "TEST", "PROD"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    db: DatabaseConfig
    testdb: TestDatabaseConfig
    mode: ModeConfig


settings = Settings()
