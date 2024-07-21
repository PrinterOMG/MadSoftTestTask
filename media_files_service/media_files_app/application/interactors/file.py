from typing import BinaryIO, Generator

from media_files_app.application.interfaces.common import UUIDGenerator
from media_files_app.application.interfaces.storage import FileStorage


class UploadFileInteractor:
    def __init__(self, storage: FileStorage, uuid_generator: UUIDGenerator):
        self._storage = storage
        self._uuid_generator = uuid_generator

    async def __call__(
        self,
        filename: str,
        file: BinaryIO,
        length: int,
        content_type: str,
    ) -> str:
        new_filename = str(self._uuid_generator())
        if '.' in filename:
            new_filename += '.' + filename.split('.')[-1]

        self._storage.upload_file(new_filename, file, length, content_type)

        return new_filename


class DownloadFileInteractor:
    def __init__(self, storage: FileStorage):
        self._storage = storage

    async def __call__(
        self,
        filename: str,
    ) -> tuple[Generator[bytes, None, None], str | None]:
        return self._storage.download_file(filename)
