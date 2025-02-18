import asyncio
import timeit
from typing import Awaitable, Callable, Any

import asyncpg
import pytest

from memes_app.config import get_config


config = get_config('tests/.env.test')


async def postgres_responsive(host: str) -> bool:
    try:
        conn = await asyncpg.connect(
            host=host,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            database=config.POSTGRES_DB,
            password=config.POSTGRES_PASSWORD,
        )
    except (ConnectionError, asyncpg.CannotConnectNowError):
        return False

    try:
        return (await conn.fetchrow('SELECT 1'))[0] == 1
    finally:
        await conn.close()


async def async_wait_until_responsive(
    check: Callable[..., Awaitable],
    timeout: float,
    pause: float,
    **kwargs: Any,
) -> None:
    ref = timeit.default_timer()
    now = ref
    while (now - ref) < timeout:
        if await check(**kwargs):
            return
        await asyncio.sleep(pause)
        now = timeit.default_timer()

    raise RuntimeError('Timeout reached while waiting on service!')


@pytest.fixture(scope='session')
async def postgres_service(docker_services):
    await async_wait_until_responsive(
        timeout=30,
        pause=0.1,
        check=postgres_responsive,
        host='localhost',
    )
