from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.settings import settings
from passlib.context import CryptContext
from jose import jwt


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class SecurityService():
    _pwd_context: CryptContext
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="user/login")


    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        

    async def get_user_info(self, token: str) -> dict:
        decoded_jwt = jwt.decode(token, settings.secret_key)
        
        if not self.verify_token(decoded_jwt):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

        return decoded_jwt


    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"expires": str(expire)})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key)
        return encoded_jwt
    

    def verify_pwd(self, user_pwd, db_hashed_pwd) -> bool:
        return self._pwd_context.verify(user_pwd, db_hashed_pwd)


    def hash_pwd(self, user_pwd) -> str:
        return self._pwd_context.hash(user_pwd)
    

    def verify_token(self, decoded: dict) -> bool:
        if not decoded["user_id"] or not decoded["expires"]:
            return False
        
        if datetime.strptime(decoded["expires"], "%Y-%m-%d %H:%M:%S.%f%z") < datetime.now(timezone.utc):
            return False

        return True