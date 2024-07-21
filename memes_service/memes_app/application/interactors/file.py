from typing import AsyncGenerator

from memes_app.application.interfaces.media_files_service_api import (
    MediaFilesServiceApiProtocol,
)


class DownloadFileInteractor:
    def __init__(
        self,
        media_files_api: MediaFilesServiceApiProtocol,
    ):
        self._media_files_api = media_files_api

    async def __call__(
        self,
        filename: str,
    ) -> tuple[AsyncGenerator[bytes], str]:
        return await self._media_files_api.download_file(filename)
