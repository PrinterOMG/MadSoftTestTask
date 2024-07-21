from datetime import datetime

from uuid import uuid4

import pytest

from memes_app.infrastructure.database.models import MemeModel


@pytest.fixture(scope='function')
async def prepared_meme(async_session_factory) -> MemeModel:
    meme = MemeModel(
        id=uuid4(),
        created_at=datetime.utcnow(),
        title='Test meme',
        description='Test meme description',
        image_url='/api/files/test.png',
    )

    async with async_session_factory.begin() as session:
        session.add(meme)

    yield meme

    async with async_session_factory.begin() as session:
        await session.delete(meme)
