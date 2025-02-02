from datetime import datetime, timedelta, timezone
from src.settings import settings
from src.infra.database.database import SqlHelper
from src.presentation.schemas.response_schema import ResponseAuthSchema, ResponseSchema
from src.infra.database.models.user import User
from src.infra.database.repository.user_repository import UserRepository
from passlib.context import CryptContext
from jose import jwt


class AuthService():
    _user_repository: UserRepository
    _pwd_context: CryptContext


    def __init__(self, repository: UserRepository):
        self._user_repository = repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    async def register_user(self, user: User) -> ResponseSchema:
        user.id = SqlHelper.new_id()
        user.hashed_password = self._pwd_context.hash(user.hashed_password)

        if (await self._user_repository.is_user_exist(user)):
            return ResponseSchema(success=False, message="User with this email already exists") 
        
        await self._user_repository.create(user)

        return ResponseSchema(success=True)
    

    async def auth_user(self, user: User) -> ResponseAuthSchema:
        db_user = await self._user_repository.get_user_by_email(user)
        if (not db_user or not self._pwd_context.verify(user.hashed_password, db_user.hashed_password)):
            return ResponseAuthSchema(success=False, message="Incorrect login data")

        jwt = self.create_access_token({
            "user_id": str(db_user.id)
        })

        return ResponseAuthSchema(success=True, access_token=jwt)
    

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=14)
        to_encode.update({"expires": str(expire)})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key)
        return encoded_jwt
    