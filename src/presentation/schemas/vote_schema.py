from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer

from .base import APIModelConfig


class VoteSchema(BaseModel):
    id: UUID
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    model_config = APIModelConfig
    
    @field_serializer("start_date")
    def serialize_start_date(self, value: datetime):
        return value.replace(tzinfo=None)
    
    @field_serializer("end_date")
    def serialize_end_date(self, value: datetime):
        return value.replace(tzinfo=None)


class VoteSchemaAdd(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    
    @field_serializer("start_date")
    def serialize_start_date(self, value: datetime):
        return value.replace(tzinfo=None)
    
    @field_serializer("end_date")
    def serialize_end_date(self, value: datetime):
        return value.replace(tzinfo=None)