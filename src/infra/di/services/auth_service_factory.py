from dishka import Provider, Scope, provide
from src.infra.database.repository.user_repository import UserRepository
from src.usecases.auth_service import AuthService


class AuthServiceFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_service(self, repository: UserRepository) -> AuthService:
        return AuthService(repository)
