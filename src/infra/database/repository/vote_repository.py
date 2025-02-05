from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.models.vote import Vote
from src.infra.protocols import AbstractSQLRepository


class VoteRepository(AbstractSQLRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Vote)
