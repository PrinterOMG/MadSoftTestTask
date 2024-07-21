from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from media_files_app.config import AppConfig, get_config
from media_files_app.controllers.http.routers.main import router
from media_files_app.ioc.main import providers


config = get_config()
async_container = make_async_container(
    *providers,
    context={
        AppConfig: config,
    },
)


def create_app() -> FastAPI:
    app = FastAPI(
        title='Media files API',
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
    )

    app.include_router(router, prefix='/api')

    setup_dishka(
        app=app,
        container=async_container,
    )

    return app
