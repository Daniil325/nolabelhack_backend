from typing import TypeVar
from uuid import UUID

from sqlalchemy import select

from src.infra.database.repository.answer_repository import AnswerRepository
from src.infra.database.repository.vote_repository import VoteRepository
from src.infra.protocols import AbstractSQLRepository


RepoType = TypeVar("RepoType", bound=AbstractSQLRepository)

class SqlReader:
    
    def __init__(self, repo: RepoType):
        self.repo = repo
        
    async def fetch_list(self):
        stmt = select(self.repo.model)
        items = (await self.repo.session.execute(stmt)).scalars().all()
        return {"items": items}
    
    async def fetch_one(self, id: UUID):
        stmt = select(self.repo.model).where(self.repo.model.id == id)
        item = (await self.repo.session.execute(stmt)).scalar_one_or_none()
        return {"item": item}
    

class VoteReader(SqlReader):
    
    def __init__(self, session):   
        super().__init__(VoteRepository(session))
        
    
class AnswerReader(SqlReader):
    
    def __init__(self, session):
        super().__init__(AnswerRepository(session))
    