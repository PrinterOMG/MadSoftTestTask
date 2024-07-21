from typing import Annotated

from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

from memes_app.application.dto.meme import NewMemeDTO, UpdateMemeDTO
from memes_app.application.interactors.meme import (
    CreateMemeInteractor,
    DeleteMemeInteractor,
    GetAllMemesInteractor,
    GetMemeByIdInteractor,
    UpdateMemeImageInteractor,
    UpdateMemeInteractor,
)
from memes_app.controllers.http.routers.dependencies import image_checker
from memes_app.controllers.schemas.common import ErrorMessage
from memes_app.controllers.schemas.meme import MemeRead, MemeUpdate
from memes_app.domain.exceptions.meme import MemeNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/',
    response_model=list[MemeRead],
)
async def get_all_memes(
    interactor: FromDishka[GetAllMemesInteractor],
):
    return await interactor()


@router.get(
    '/{meme_id}',
    response_model=MemeRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Meme not found',
            'model': ErrorMessage,
        },
    },
)
async def get_meme_by_id(
    meme_id: UUID,
    *,
    interactor: FromDishka[GetMemeByIdInteractor],
):
    try:
        return await interactor(meme_id=str(meme_id))
    except MemeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with id "{meme_id}" not found',
        )


@router.post(
    '',
    response_model=MemeRead,
)
async def create_meme(
    meme_image: Annotated[UploadFile, Depends(image_checker)],
    meme_title: Annotated[str, Form(min_length=3, max_length=100)],
    meme_description: Annotated[str, Form(min_length=3, max_length=1000)],
    *,
    interactor: FromDishka[CreateMemeInteractor],
):
    return await interactor(
        NewMemeDTO(
            title=meme_title,
            description=meme_description,
        ),
        image_file=meme_image.file,
        image_filename=meme_image.filename,
        image_content_type=meme_image.content_type,
    )


@router.put(
    '/{meme_id}',
    response_model=MemeRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Meme not found',
            'model': ErrorMessage,
        },
    },
)
async def update_meme(
    meme_id: UUID,
    meme_update: MemeUpdate,
    *,
    interactor: FromDishka[UpdateMemeInteractor],
):
    try:
        return await interactor(
            UpdateMemeDTO(
                id=str(meme_id),
                title=meme_update.title,
                description=meme_update.description,
            ),
        )
    except MemeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with id "{meme_id}" not found',
        )


@router.patch(
    '/{meme_id}/update_image',
    response_model=MemeRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Meme not found',
            'model': ErrorMessage,
        },
    },
)
async def update_meme_image(
    meme_id: UUID,
    meme_image: Annotated[UploadFile, Depends(image_checker)],
    *,
    interactor: FromDishka[UpdateMemeImageInteractor],
):
    try:
        return await interactor(
            meme_id=str(meme_id),
            image_file=meme_image.file,
            image_filename=meme_image.filename,
            image_content_type=meme_image.content_type,
        )
    except MemeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with id "{meme_id}" not found',
        )


@router.delete(
    '/{meme_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_meme(
    meme_id: UUID,
    *,
    interactor: FromDishka[DeleteMemeInteractor],
):
    await interactor(meme_id=str(meme_id))
