from uuid import UUID
from fastapi import HTTPException, status
from src.presentation.schemas.response_schema import ResponseAuthSchema, BaseResponseSchema
from src.infra.database.models.user import User
from src.infra.database.repository.user_repository import UserRepository
from src.presentation.schemas.user_schema import UserRead
from src.usecases.security_service import SecurityService


class AuthService():
    _user_repository: UserRepository
    _security_service: SecurityService

    def __init__(self, repository: UserRepository, security_service: SecurityService):
        self._user_repository = repository
        self._security_service = security_service

    async def register_user(self, user: User) -> BaseResponseSchema:
        user.id = self._user_repository.new_id()
        user.hashed_password = self._security_service.hash_pwd(
            user.hashed_password)

        if (await self._user_repository.is_user_exist(user)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists")

        await self._user_repository.create(user)

        return BaseResponseSchema(success=True)

    async def auth_user(self, user: User) -> ResponseAuthSchema:

        db_user = await self._user_repository.get_user_by_email(user)
        if (not db_user or not self._security_service.verify_pwd(user.hashed_password, db_user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect username or password")

        jwt = self._security_service.create_access_token({
            "user_id": str(db_user.id)
        })

        return ResponseAuthSchema(success=True, access_token=jwt)

    async def get_user_by_id(self, id: UUID) -> UserRead:

        user = await self._user_repository.get(id)

        return UserRead(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
