from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, UploadFile, status
from starlette.responses import StreamingResponse

from media_files_app.application.interactors.file import (
    DownloadFileInteractor,
    UploadFileInteractor,
)
from media_files_app.domain.exceptions.storage import FileNotFoundInStorageError


router = APIRouter(route_class=DishkaRoute)


@router.post('/upload')
async def upload_file(
    file: UploadFile,
    *,
    interactor: FromDishka[UploadFileInteractor],
):
    filename = await interactor(file.filename, file.file, file.size, file.content_type)
    return {'filename': filename}


@router.get('/download/{filename}')
async def download_file(
    filename: str,
    *,
    interactor: FromDishka[DownloadFileInteractor],
):
    try:
        file, content_type = await interactor(filename)
    except FileNotFoundInStorageError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )

    return StreamingResponse(file, media_type=content_type)
