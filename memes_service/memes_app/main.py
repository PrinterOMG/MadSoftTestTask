from fastapi import FastAPI

from memes_app.config import get_config


def create_app() -> FastAPI:
    config = get_config(env_file='../.env')  # noqa

    app = FastAPI(
        title='Memes API',
    )

    return app
