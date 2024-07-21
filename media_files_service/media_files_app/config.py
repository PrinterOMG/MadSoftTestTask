from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        frozen=True,
    )

    MINIO_URL: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str


@lru_cache
def get_config(env_file: str = '.env') -> AppConfig:
    return AppConfig(_env_file=env_file)
