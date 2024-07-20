from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from memes_app.config import AppConfig


def new_session_maker(
    config: AppConfig,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        config.database_uri,
        pool_size=15,
        max_overflow=15,
    )

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
