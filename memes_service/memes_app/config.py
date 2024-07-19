from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        frozen=True,
    )


@lru_cache
def get_config(env_file: str = '.env') -> Config:
    return Config(_env_file=env_file)
