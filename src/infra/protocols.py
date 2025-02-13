from abc import ABC, abstractmethod
from typing import Any, BinaryIO, Generic, TypeVar, Protocol
import uuid

from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

T = TypeVar("T")


class AbstractSQLRepository(Generic[T], Protocol):

    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars()

    async def get(self, id: UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, item: T) -> None:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update(self, changes: dict[str, Any], id: UUID) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**changes)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, id: UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

    @staticmethod
    def new_id() -> UUID:
        return uuid.uuid4()


class ImageStorage(ABC):

    @abstractmethod
    async def exists(self, image_id: str) -> bool:
        ...

    @abstractmethod
    async def upload(self, filename: str, file: BinaryIO, size: int | None = None) -> str:
        ...

    @abstractmethod
    async def download(self, image_id: str) -> bytes:
        ...
