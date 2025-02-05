from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from fastapi_users import models


class UserCreate(schemas.BaseUserCreate):
    is_verified: Optional[bool] = True

    is_active: None = None
    is_superuser: None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(schemas.BaseUser):
    first_name: str | None
    last_name: str | None
