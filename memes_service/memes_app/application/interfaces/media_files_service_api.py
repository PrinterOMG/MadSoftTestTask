from typing import AsyncGenerator, BinaryIO

from abc import abstractmethod


class MediaFilesServiceApiProtocol:
    @abstractmethod
    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        content_type: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def download_file(
        self,
        filename: str,
        chunk_size: int = 64 * 1024,
    ) -> tuple[AsyncGenerator[bytes, None], str]:
        raise NotImplementedError
