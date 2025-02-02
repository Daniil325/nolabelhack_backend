from fastapi import APIRouter, Response
from dishka.integrations.fastapi import (
    FromDishka, inject
)

from src.presentation.schemas.response_schema import ResponseAuthSchema, ResponseSchema
from src.infra.database.models.user import User
from src.presentation.schemas.user_schema import UserCreate, UserLogin
from src.usecases.auth_service import AuthService

router = APIRouter()


@router.get("/login")
async def get_user_login_page():
    return {"gol": True}


@router.post("/login", response_model=ResponseAuthSchema)
@inject
async def user_login(
    response: Response, 
    user: UserLogin,
    auth_service: FromDishka[AuthService]
):
    user_model = User(
        email=user.email,
        hashed_password=user.password
    )

    result = await auth_service.auth_user(user_model)

    return result


@router.get("/registration")
async def get_user_registration_page():
    return {"gol": True}


@router.post("/registration", response_model=ResponseSchema)
@inject
async def user_registration(user: UserCreate, auth_service: FromDishka[AuthService]):
    user_model = User(
        email=user.email,
        hashed_password=user.password
    )

    response = await auth_service.register_user(user_model)

    return response


@router.get("/profile")
async def get_user_profile_page():
    #можно сделать через получение объекта юзера и вытягивания его ид
    return {"gol": True}


@router.put("/profile")
async def change_user_profile():
    return {"gol": True}