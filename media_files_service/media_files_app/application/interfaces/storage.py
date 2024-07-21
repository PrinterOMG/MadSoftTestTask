from abc import abstractmethod
from typing import BinaryIO, Generator, Protocol


class FileStorage(Protocol):
    @abstractmethod
    def upload_file(
        self,
        name: str,
        file: BinaryIO,
        length: int,
        content_type: str = 'application/octet-stream',
    ):
        raise NotImplementedError

    @abstractmethod
    def download_file(
        self,
        name: str,
        chunk_size: int = 64 * 1024,
    ) -> tuple[Generator[bytes, None, None], str | None]:
        """
        :param chunk_size:
        :param name:
        :return:
        :raises FileNotFoundInStorageError:
        """
        raise NotImplementedError
