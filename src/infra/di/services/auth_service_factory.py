from dishka import Provider, Scope, provide
from src.infra.database.repository.user_repository import UserRepository
from src.usecases.auth_service import AuthService
from src.usecases.security_service import SecurityService


class AuthServiceFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_service(self, repository: UserRepository, security_service: SecurityService) -> AuthService:
        return AuthService(repository, security_service)
