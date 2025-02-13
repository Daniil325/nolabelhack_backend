from dishka import Provider, Scope, provide
from src.usecases.security_service import SecurityService


class SecurityServiceFactory(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_security_service(self) -> SecurityService:
        return SecurityService()
