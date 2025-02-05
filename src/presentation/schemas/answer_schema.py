from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_serializer

from .base import APIModelConfig


class AnswerSchema(BaseModel):
    id: UUID
    answer_text: str
    vote_id: UUID
    model_config = APIModelConfig


class AnswerSchemaAdd(BaseModel):
    answer_text: str
    vote_id: UUID
    created_at: datetime
    model_config = APIModelConfig

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return value.replace(tzinfo=None)
