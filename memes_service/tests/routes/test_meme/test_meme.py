from uuid import uuid4

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from memes_app.infrastructure.database.models import MemeModel


async def test_get_meme(
    ac: AsyncClient,
    prepared_meme: MemeModel,
    async_session_factory: async_sessionmaker,
):
    response = await ac.get(f'api/memes/{prepared_meme.id}')

    assert response.status_code == 200, f'Wrong status code: {response.status_code}'

    json_response = response.json()
    assert json_response == {
        'id': str(prepared_meme.id),
        'created_at': prepared_meme.created_at.isoformat(),
        'title': prepared_meme.title,
        'description': prepared_meme.description,
        'image_url': prepared_meme.image_url,
    }, f'Wrong response: {json_response}'


async def test_get_bad_meme(
    ac: AsyncClient,
):
    response = await ac.get(f'api/memes/{uuid4()}')

    assert response.status_code == 404, f'Wrong status code: {response.status_code}'


async def test_create_meme(
    ac: AsyncClient,
    async_session_factory: async_sessionmaker,
):
    files = {
        'image': ('test.png', open('tests/images/test.png', 'rb'), 'image/png'),
    }
    data = {
        'meme_title': 'test title',
        'meme_description': 'test description',
    }
    response = await ac.post(
        'api/memes',
        data=data,
        files=files,
    )

    assert response.status_code == 200, f'Wrong status code: {response.text}'

    json_response = response.json()
    assert json_response == {
        'id': str(json_response['id']),
        'created_at': json_response['created_at'],
        'title': data['meme_title'],
        'description': data['meme_description'],
        'image_url': '/api/files/saved_mock.png',
    }, f'Wrong response: {json_response}'

    async with async_session_factory() as session:
        db_meme = await session.get(MemeModel, json_response['id'])
        assert db_meme, 'Meme not found in database'

        assert json_response == {
            'id': str(db_meme.id),
            'created_at': db_meme.created_at.isoformat(),
            'title': data['meme_title'],
            'description': data['meme_description'],
            'image_url': '/api/files/saved_mock.png',
        }, 'Wrong meme in database'


async def test_meme_update(
    ac: AsyncClient,
    prepared_meme: MemeModel,
    async_session_factory: async_sessionmaker,
):
    update_data = {
        'title': 'test update title',
        'description': 'test update description',
    }
    response = await ac.put(
        f'api/memes/{prepared_meme.id}',
        json=update_data,
    )

    assert response.status_code == 200, f'Wrong status code: {response.text}'

    json_response = response.json()
    assert json_response == {
        'id': str(json_response['id']),
        'created_at': json_response['created_at'],
        'title': update_data['title'],
        'description': update_data['description'],
        'image_url': '/api/files/test.png',
    }

    async with async_session_factory() as session:
        db_meme = await session.get(MemeModel, json_response['id'])
        assert db_meme, 'Meme not found in database'

        assert json_response == {
            'id': str(db_meme.id),
            'created_at': db_meme.created_at.isoformat(),
            'title': update_data['title'],
            'description': update_data['description'],
            'image_url': '/api/files/test.png',
        }, 'Wrong meme in database'


async def test_update_bad_meme(
    ac: AsyncClient,
):
    update_data = {
        'title': 'test update title',
        'description': 'test update description',
    }
    response = await ac.put(
        f'api/memes/{uuid4()}',
        json=update_data,
    )

    assert response.status_code == 404, f'Wrong status code: {response.text}'


async def test_update_meme_image(
    ac: AsyncClient,
    prepared_meme: MemeModel,
    async_session_factory: async_sessionmaker,
):
    files = {
        'image': ('test.png', open('tests/images/test.png', 'rb'), 'image/png'),
    }
    response = await ac.patch(
        f'api/memes/{prepared_meme.id}/update_image',
        files=files,
    )

    assert response.status_code == 200, f'Wrong status code: {response.text}'

    json_response = response.json()
    assert json_response == {
        'id': str(json_response['id']),
        'created_at': json_response['created_at'],
        'title': prepared_meme.title,
        'description': prepared_meme.description,
        'image_url': '/api/files/saved_mock.png',
    }

    async with async_session_factory() as session:
        db_meme = await session.get(MemeModel, json_response['id'])
        assert db_meme, 'Meme not found in database'

        assert json_response == {
            'id': str(db_meme.id),
            'created_at': db_meme.created_at.isoformat(),
            'title': db_meme.title,
            'description': db_meme.description,
            'image_url': '/api/files/saved_mock.png',
        }, 'Wrong meme in database'


async def test_update_image_bad_meme(
    ac: AsyncClient,
):
    files = {
        'image': ('test.png', open('tests/images/test.png', 'rb'), 'image/png'),
    }
    response = await ac.patch(
        f'api/memes/{uuid4()}/update_image',
        files=files,
    )

    assert response.status_code == 404, f'Wrong status code: {response.text}'


async def test_delete_meme(
    ac: AsyncClient,
    prepared_meme: MemeModel,
    async_session_factory: async_sessionmaker,
):
    response = await ac.delete(f'api/memes/{prepared_meme.id}')

    assert response.status_code == 204, f'Wrong status code: {response.text}'

    async with async_session_factory() as session:
        db_meme = await session.get(MemeModel, prepared_meme.id)
        assert not db_meme, 'Meme not deleted from database'


async def test_delete_bad_meme(
    ac: AsyncClient,
):
    response = await ac.delete(f'api/memes/{uuid4()}')

    assert response.status_code == 204, f'Wrong status code: {response.text}'
