from unittest.mock import AsyncMock, Mock

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from memes_app.application.interfaces.media_files_service_api import (
    MediaFilesServiceApiProtocol,
)
from memes_app.config import AppConfig, get_config
from memes_app.infrastructure.database.models.base import BaseModel
from memes_app.ioc.gateways import GatewaysProvider
from memes_app.ioc.interactors import InteractorsProvider
from memes_app.ioc.main import AppProvider
from memes_app.main import create_app


pytest_plugins = ['tests.docker_services']


@pytest.fixture
async def db_engine(container) -> AsyncEngine:
    return await container.get(AsyncEngine)


@pytest.fixture
async def async_session_factory(container) -> async_sessionmaker[AsyncSession]:
    return await container.get(async_sessionmaker[AsyncSession])


@pytest.fixture(scope='session')
def config() -> AppConfig:
    return get_config(env_file='tests/.env.test')


class MockMediaFilesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_media_files_api(
        self,
    ) -> MediaFilesServiceApiProtocol:
        media_files_api = Mock()

        media_files_api.upload_file = AsyncMock(return_value='saved_mock.png')

        media_files_api.download_file = AsyncMock()

        return media_files_api


@pytest.fixture
async def container(config) -> AsyncContainer:
    container = make_async_container(
        AppProvider(),
        GatewaysProvider(),
        InteractorsProvider(),
        MockMediaFilesProvider(),
        context={
            AppConfig: config,
        },
    )
    yield container
    await container.close()


@pytest.fixture(autouse=True)
async def prepare_database(postgres_service, db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture
def app(container) -> FastAPI:
    app = create_app()
    setup_dishka(container=container, app=app)
    return app


@pytest.fixture
async def ac(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
