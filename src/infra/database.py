from typing import Any, Generic, TypeVar
import uuid
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.protocols import AbstractSQLRepository

T = TypeVar("T")


class SqlHelper(AbstractSQLRepository[T]):

    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    @staticmethod
    def new_id() -> UUID:
        return uuid.uuid4()

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars()

    async def get_by_id(self, id: UUID) -> T | None:
        stmt = select(T).where(T.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, item: T) -> None:
        self.session.add(item)
        await self.session.commit()

    async def update(self, changes: dict[str, Any], id: UUID) -> None:
        stmt = update(T).where(self.model.id == id).values(**changes)
        self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, id: UUID) -> None:
        stmt = delete(T).where(T.id == id)
        self.session.execute(stmt)
        await self.session.commit()
        