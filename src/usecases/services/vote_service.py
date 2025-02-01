from src.infra.database.database import SqlHelper
from src.presentation.schemas.vote_schema import VoteSchema, VoteSchemaAdd
from src.infra.database.models.vote import Vote
from src.infra.database.repository.vote_repository import VoteRepository


class VoteService():
    _vote_repository: VoteRepository

    def __init__(self, repository: VoteRepository):
        self._vote_repository = repository

    async def get_vote_list(self) -> list[Vote]:
        return (await self._vote_repository.get_all())
    
    async def add_vote(self, vote: VoteSchemaAdd) -> VoteSchema:
        #todo refactor this

        vote_model = Vote()
        vote_model.id = SqlHelper.new_id()
        vote_model.title = vote.title
        vote_model.description = vote.description
        vote_model.start_date = vote.start_date.replace(tzinfo=None)
        vote_model.end_date = vote.end_date.replace(tzinfo=None)
        vote_model.is_active = vote.is_active

        vote_model = await self._vote_repository.create(vote_model)
        
        return vote_model