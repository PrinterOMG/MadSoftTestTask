from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        frozen=True,
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int = 5432

    MEDIA_FILES_API_URL: str

    @computed_field  # type: ignore[misc]
    @property
    def database_uri(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )


@lru_cache
def get_config(env_file: str = '.env') -> AppConfig:
    return AppConfig(_env_file=env_file)
