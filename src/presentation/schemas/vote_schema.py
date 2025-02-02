from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class VoteSchema(BaseModel):
    id: UUID
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool


class VoteSchemaAdd(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool