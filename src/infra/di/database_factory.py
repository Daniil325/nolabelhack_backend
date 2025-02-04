from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.database.database import Database


class DatabaseFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self) -> Database:
        return Database()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, db: Database) -> AsyncSession:
        return await db.get_session()
