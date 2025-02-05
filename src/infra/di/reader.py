from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.reader import AnswerReader, VoteReader


class ReaderProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    @provide
    def get_vote_reader(self, session: AsyncSession) -> VoteReader:
        return VoteReader(session)

    @provide
    def get_answer_reader(self, session: AsyncSession) -> AnswerReader:
        return AnswerReader(session)
