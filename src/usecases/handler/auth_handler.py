from typing import Annotated
from dishka.integrations.fastapi import (
    FromDishka, inject
)
from fastapi import Depends, HTTPException, status
from src.presentation.schemas.user_schema import UserRead
from src.usecases.auth_service import AuthService
from src.usecases.security_service import SecurityService


class AuthHandler():
    @staticmethod
    @inject
    async def get_current_user(
        token: Annotated[str, Depends(SecurityService.oauth2_scheme)],
        auth_service: FromDishka[AuthService],
        security_service: FromDishka[SecurityService]
    ) -> UserRead:

        current_user_info = await security_service.get_user_info(token)

        current_user = await auth_service.get_user_by_id(current_user_info["user_id"])

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to extract credentials",
            )

        return current_user
