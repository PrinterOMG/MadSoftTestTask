from typing import AsyncIterable
import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, from_context, provide

from memes_app.application.interfaces.common import DateTimeNowGenerator, UUIDGenerator
from memes_app.application.interfaces.unit_of_work import UnitOfWork
from memes_app.config import AppConfig
from memes_app.infrastructure.database.database import new_session_maker
from memes_app.ioc.gateways import GatewaysProvider
from memes_app.ioc.interactors import InteractorsProvider


class AppProvider(Provider):
    config = from_context(provides=AppConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_datetime_now_generator(self) -> DateTimeNowGenerator:
        return dt.datetime.utcnow

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(
        self,
        config: AppConfig,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config=config)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, UnitOfWork]]:
        async with async_session_maker() as session:
            yield session


providers = (
    AppProvider(),
    GatewaysProvider(),
    InteractorsProvider(),
)
