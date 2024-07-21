from typing import BinaryIO

from memes_app.application.dto.meme import NewMemeDTO, UpdateMemeDTO
from memes_app.application.interfaces.common import DateTimeNowGenerator, UUIDGenerator
from memes_app.application.interfaces.media_files_service_api import (
    MediaFilesServiceApiProtocol,
)
from memes_app.application.interfaces.meme import (
    MemeDeleter,
    MemeGatewayProtocol,
    MemeReader,
    MemeSaver,
)
from memes_app.application.interfaces.unit_of_work import UnitOfWork
from memes_app.domain.entities.meme import MemeEntity
from memes_app.domain.exceptions.meme import MemeNotFoundError


class GetMemeByIdInteractor:
    def __init__(
        self,
        meme_gateway: MemeReader,
    ):
        self._meme_gateway = meme_gateway

    async def __call__(self, meme_id: str) -> MemeEntity:
        """
        :param meme_id:
        :return:
        :raise MemeNotFoundError:
        """
        meme = await self._meme_gateway.get_by_id(meme_id)
        if meme is None:
            raise MemeNotFoundError
        return meme


class GetAllMemesInteractor:
    def __init__(
        self,
        meme_gateway: MemeReader,
    ):
        self._meme_gateway = meme_gateway

    async def __call__(self, limit: int, offset: int) -> list[MemeEntity]:
        return await self._meme_gateway.get_all(limit=limit, offset=offset)


class CreateMemeInteractor:
    def __init__(
        self,
        meme_gateway: MemeSaver,
        uuid_generator: UUIDGenerator,
        datetime_now_generator: DateTimeNowGenerator,
        media_files_service_api: MediaFilesServiceApiProtocol,
        uow: UnitOfWork,
    ):
        self._meme_gateway = meme_gateway
        self._uuid_generator = uuid_generator
        self._datetime_now_generator = datetime_now_generator
        self._media_files_service_api = media_files_service_api
        self._uow = uow

    async def __call__(
        self,
        meme: NewMemeDTO,
        image_file: BinaryIO,
        image_filename: str,
        image_content_type: str,
    ) -> MemeEntity:
        filename = await self._media_files_service_api.upload_file(
            file=image_file,
            filename=image_filename,
            content_type=image_content_type,
        )

        new_meme = MemeEntity(
            id=self._uuid_generator(),
            title=meme.title,
            description=meme.description,
            image_url=f'/api/files/{filename}',
            created_at=self._datetime_now_generator(),
        )

        await self._meme_gateway.save(new_meme)
        await self._uow.commit()

        return new_meme


class UpdateMemeInteractor:
    def __init__(
        self,
        meme_gateway: MemeGatewayProtocol,
        uow: UnitOfWork,
    ):
        self._meme_gateway = meme_gateway
        self._uow = uow

    async def __call__(self, meme_update: UpdateMemeDTO) -> MemeEntity:
        """
        :param meme_update:
        :return:
        :raises MemeNotFoundError:
        """
        meme = await self._meme_gateway.get_by_id(meme_update.id)
        if meme is None:
            raise MemeNotFoundError

        meme.title = meme_update.title
        meme.description = meme_update.description

        await self._meme_gateway.update(meme)
        await self._uow.commit()

        return meme


class UpdateMemeImageInteractor:
    def __init__(
        self,
        meme_gateway: MemeGatewayProtocol,
        uow: UnitOfWork,
        media_files_service_api: MediaFilesServiceApiProtocol,
    ):
        self._meme_gateway = meme_gateway
        self._uow = uow
        self._media_files_service_api = media_files_service_api

    async def __call__(
        self,
        meme_id: str,
        image_file: BinaryIO,
        image_filename: str,
        image_content_type: str,
    ) -> MemeEntity:
        meme = await self._meme_gateway.get_by_id(meme_id)
        if meme is None:
            raise MemeNotFoundError

        filename = await self._media_files_service_api.upload_file(
            file=image_file,
            filename=image_filename,
            content_type=image_content_type,
        )

        meme.image_url = f'/api/files/{filename}'

        await self._meme_gateway.update(meme)
        await self._uow.commit()

        return meme


class DeleteMemeInteractor:
    def __init__(
        self,
        meme_gateway: MemeDeleter,
        uow: UnitOfWork,
    ):
        self._meme_gateway = meme_gateway
        self._uow = uow

    async def __call__(self, meme_id: str) -> None:
        await self._meme_gateway.delete(meme_id)
        await self._uow.commit()
