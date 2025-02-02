from dishka import Provider, Scope, provide
from src.infra.database.repository.vote_repository import VoteRepository
from src.usecases.services.vote_service import VoteService


class VoteServiceFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_vote_service(self, repository: VoteRepository) -> VoteService:
        return VoteService(repository)
