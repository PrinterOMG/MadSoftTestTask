import aiohttp

from typing import AsyncGenerator, BinaryIO

from aiohttp import ClientSession

from memes_app.application.interfaces.media_files_service_api import (
    MediaFilesServiceApiProtocol,
)
from memes_app.domain.exceptions.media_files_service import (
    FileNotFoundInMediaFilesServiceError,
)


class MediaFilesServiceApi(MediaFilesServiceApiProtocol):
    def __init__(self, media_files_api_url: str, session: ClientSession):
        self._media_files_api_url = media_files_api_url
        self._session = session

    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
        content_type: str,
    ) -> str:
        url = self._media_files_api_url + '/api/files/upload'

        data = aiohttp.FormData()
        data.add_field(
            'file',
            file,
            filename=filename,
            content_type=content_type,
        )

        async with self._session.post(url, data=data) as response:
            response.raise_for_status()

            return (await response.json())['filename']

    async def download_file(
        self,
        filename: str,
        chunk_size: int = 64 * 1024,
    ) -> tuple[AsyncGenerator[bytes], str]:
        url = self._media_files_api_url + '/api/files/download/' + filename

        # Не используем контекстный менеджер, чтобы не закрылось соединение
        response = await self._session.get(url, timeout=aiohttp.ClientTimeout(total=30))
        if response.status == 404:
            raise FileNotFoundInMediaFilesServiceError

        response.raise_for_status()

        # Оборачиваем в асинхронный генератор, чтобы было удобнее обрабатывать ошибки
        async def file_generator() -> AsyncGenerator[bytes]:
            try:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            finally:
                # Закрываем соединение вручную
                await response.release()

        return file_generator(), response.content_type
