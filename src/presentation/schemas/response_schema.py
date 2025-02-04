from typing import Optional
from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    success: bool
    message: Optional[str] = ""

class ResponseAuthSchema(BaseResponseSchema):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    