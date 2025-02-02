from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.database.repository.user_repository import UserRepository
from src.infra.database.models.user import User


class UserRepositoryFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session, model=User)
