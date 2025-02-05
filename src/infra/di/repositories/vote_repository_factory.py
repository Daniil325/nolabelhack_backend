from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repository.vote_repository import VoteRepository


class VoteRepositoryFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_vote_repository(self, session: AsyncSession) -> VoteRepository:
        return VoteRepository(session=session)
