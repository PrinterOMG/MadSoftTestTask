from abc import abstractmethod
from typing import Protocol

from memes_app.domain.entities.meme import MemeEntity


class MemeReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: str) -> MemeEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[MemeEntity]:
        raise NotImplementedError


class MemeSaver(Protocol):
    @abstractmethod
    async def save(self, meme: MemeEntity) -> None:
        raise NotImplementedError


class MemeUpdater(Protocol):
    @abstractmethod
    async def update(self, meme: MemeEntity) -> None:
        raise NotImplementedError


class MemeDeleter(Protocol):
    @abstractmethod
    async def delete(self, meme_id: str) -> None:
        raise NotImplementedError


class MemeGatewayProtocol(
    MemeReader,
    MemeSaver,
    MemeUpdater,
    MemeDeleter,
    Protocol,
): ...
