from typing import Annotated
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import (
    FromDishka, inject
)
from fastapi.security import OAuth2PasswordRequestForm
from src.presentation.schemas.response_schema import ResponseAuthSchema, BaseResponseSchema
from src.infra.database.models.user import User
from src.presentation.schemas.user_schema import UserCreate, UserRead
from src.usecases.auth_service import AuthService
from src.usecases.handler.auth_handler import AuthHandler

router = APIRouter()


@router.post("/login", response_model=ResponseAuthSchema)
@inject
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: FromDishka[AuthService]
):
    user_model = User(
        email=form_data.username,
        hashed_password=form_data.password
    )

    result = await auth_service.auth_user(user_model)

    return result


@router.post("/registration", response_model=BaseResponseSchema)
@inject
async def user_registration(
    user: UserCreate, 
    auth_service: FromDishka[AuthService]
):
    user_model = User(
        email=user.email,
        hashed_password=user.password
    )

    response = await auth_service.register_user(user_model)

    return response


@router.get("/profile", response_model=UserRead)
async def get_user_profile_page(
    current_user: Annotated[UserRead, Depends(AuthHandler.get_current_user)]
):
    return current_user


@router.put("/profile")
async def change_user_profile():
    return {"gol": True}