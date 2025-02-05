from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repository.answer_repository import AnswerRepository


class AnswerRepositoryFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_answer_repository(self, session: AsyncSession) -> AnswerRepository:
        return AnswerRepository(session=session)
