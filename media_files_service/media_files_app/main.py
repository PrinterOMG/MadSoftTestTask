from fastapi import FastAPI

from media_files_app.config import get_config


def create_app() -> FastAPI:
    config = get_config(env_file='../.env')  # noqa

    app = FastAPI(
        title='Media files API',
    )

    return app
