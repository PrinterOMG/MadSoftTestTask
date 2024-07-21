from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from memes_app.config import AppConfig, get_config
from memes_app.controllers.http.routers.main import router
from memes_app.ioc.main import providers


def create_app() -> FastAPI:
    app = FastAPI(
        title='Memes API',
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
    )

    app.include_router(router, prefix='/api')

    return app


def create_production_app() -> FastAPI:
    app = create_app()

    config = get_config()
    async_container = make_async_container(
        *providers,
        context={
            AppConfig: config,
        },
    )

    setup_dishka(
        app=app,
        container=async_container,
    )

    return app
