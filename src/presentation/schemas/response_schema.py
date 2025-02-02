from typing import Optional
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    success: bool
    message: Optional[str] = ""

class ResponseAuthSchema(ResponseSchema):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None