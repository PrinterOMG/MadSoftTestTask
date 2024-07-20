from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from memes_app.application.interfaces.meme import (
    MemeDeleter,
    MemeReader,
    MemeSaver,
    MemeUpdater,
)
from memes_app.domain.entities.meme import MemeEntity
from memes_app.infrastructure.database.models import MemeModel


class MemeGateway(MemeReader, MemeSaver, MemeUpdater, MemeDeleter):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _db_to_entity(self, db_meme: MemeModel | None) -> MemeEntity | None:
        if db_meme is None:
            return None

        return MemeEntity(
            id=str(db_meme.id),
            title=db_meme.title,
            description=db_meme.description,
            created_at=db_meme.created_at,
        )

    async def get_by_id(self, id: str) -> MemeEntity | None:
        meme = await self._session.get(MemeModel, id)
        return self._db_to_entity(meme)

    async def get_all(self) -> list[MemeEntity]:
        memes = await self._session.scalars(
            select(MemeModel),
        )
        return [self._db_to_entity(meme) for meme in memes]

    async def save(self, meme: MemeEntity) -> None:
        await self._session.execute(
            insert(MemeModel).values(
                id=meme.id,
                title=meme.title,
                description=meme.description,
                created_at=meme.created_at,
            ),
        )

    async def update(self, meme: MemeEntity) -> None:
        await self._session.execute(
            update(MemeModel)
            .where(MemeModel.id == meme.id)
            .values(
                title=meme.title,
                description=meme.description,
            ),
        )

    async def delete(self, meme_id: str) -> None:
        await self._session.execute(
            delete(MemeModel).where(MemeModel.id == meme_id),
        )
