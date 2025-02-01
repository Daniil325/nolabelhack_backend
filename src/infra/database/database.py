from typing import Any, AsyncGenerator, Generic, TypeVar
import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.infra.protocols import AbstractSQLRepository
from src.settings import settings

T = TypeVar("T")


class Database:
    _instance = None
    _connection: AsyncSession

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_db()

        return cls._instance

    def init_db(self):
        self.engine = create_async_engine(settings.db_settings.db_url)
        self._connection = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        return self._connection()


class SqlHelper(AbstractSQLRepository[T]):

    @staticmethod
    def new_id() -> UUID:
        return uuid.uuid4()
        