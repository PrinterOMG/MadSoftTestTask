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
    """
    Saves a file and returns the name of the saved file.

    ! Filename is generated on the server side using original file extension. Content type is saved too.
    """
    filename = await interactor(file.filename, file.file, file.size, file.content_type)
    return {'filename': filename}


@router.get(
    '/download/{filename}',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'File not found',
        },
    },
)
async def download_file(
    filename: str,
    *,
    interactor: FromDishka[DownloadFileInteractor],
):
    """
    Returns a file by its name
    """
    try:
        file, content_type = await interactor(filename)
    except FileNotFoundInStorageError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )

    return StreamingResponse(file, media_type=content_type)
