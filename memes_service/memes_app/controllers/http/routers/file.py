from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status
from starlette.responses import StreamingResponse

from memes_app.application.interactors.file import DownloadFileInteractor
from memes_app.domain.exceptions.media_files_service import (
    FileNotFoundInMediaFilesServiceError,
)


router = APIRouter(route_class=DishkaRoute)


@router.get('/{filename}')
async def download_file(
    filename: str,
    *,
    interactor: FromDishka[DownloadFileInteractor],
):
    """
    Returning a file by its name
    """
    try:
        file, content_type = await interactor(filename)
        return StreamingResponse(file, media_type=content_type)
    except FileNotFoundInMediaFilesServiceError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )
