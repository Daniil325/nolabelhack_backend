from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.models.answer import Answer
from src.infra.protocols import AbstractSQLRepository


class AnswerRepository(AbstractSQLRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)
