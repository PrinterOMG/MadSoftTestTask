from typing import BinaryIO, Generator

from minio import Minio, S3Error

from media_files_app.application.interfaces.storage import FileStorage
from media_files_app.domain.exceptions.storage import FileNotFoundInStorageError


class MinIoFileStorage(FileStorage):
    def __init__(self, client: Minio, bucket_name: str):
        self._client = client
        self._bucket_name = bucket_name

    def upload_file(
        self,
        name: str,
        file: BinaryIO,
        length: int,
        content_type: str = 'application/octet-stream',
    ):
        return self._client.put_object(
            self._bucket_name,
            name,
            file,
            length,
            content_type=content_type,
        )

    def download_file(
        self,
        name: str,
        chunk_size: int = 64 * 1024,
    ) -> tuple[Generator[bytes, None, None], str | None]:
        try:
            info = self._client.stat_object(self._bucket_name, name)
        except S3Error as e:
            if e.code == 'NoSuchKey':
                raise FileNotFoundInStorageError
            raise

        total_size = info.size

        def file_generator() -> Generator[bytes, None, None]:
            offset = 0
            while True:
                response = self._client.get_object(
                    self._bucket_name,
                    name,
                    offset=offset,
                    length=chunk_size,
                )
                yield response.read()
                offset += chunk_size
                if offset >= total_size:
                    break

        return file_generator(), info.content_type
