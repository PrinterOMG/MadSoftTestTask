from uuid import uuid4

from dishka import Provider, Scope, from_context, provide
from minio import Minio

from media_files_app.application.interfaces.common import UUIDGenerator
from media_files_app.application.interfaces.storage import FileStorage
from media_files_app.config import AppConfig
from media_files_app.infrastructure.storage import MinIoFileStorage
from media_files_app.ioc.interactors import InteractorsProvider


class AppProvider(Provider):
    config = from_context(provides=AppConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_minio_client(self, config: AppConfig) -> Minio:
        return Minio(
            config.MINIO_URL,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False,
        )

    @provide(scope=Scope.APP)
    def get_file_storage(self, config: AppConfig) -> FileStorage:
        return MinIoFileStorage(
            client=self.get_minio_client(config),
            bucket_name=config.MINIO_BUCKET,
        )


providers = (
    AppProvider(),
    InteractorsProvider(),
)
