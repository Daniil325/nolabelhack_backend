from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from src.infra.database.models.answer import Answer
from src.infra.database.repository.answer_repository import AnswerRepository


@dataclass
class CreateAnswerDto:
    answer_text: str
    vote_id: UUID
    created_at: datetime


@dataclass
class CreateAnswerCommand:
    answer_repo: AnswerRepository
    
    async def __call__(self, dto: CreateAnswerDto) -> str:
        identity = self.answer_repo.new_id()
        answer = Answer(
            id=identity,
            answer_text=dto.answer_text,
            created_at=dto.created_at.replace(tzinfo=None   ),
            vote_id=dto.vote_id
        )
        await self.answer_repo.create(answer)
        return identity
    

@dataclass
class UpdateAnswerCommand:
    answer_repo: AnswerRepository
    
    async def __call__(self, id: UUID, update_obj: dict[str, Any]) -> str:
        await self.answer_repo.update(update_obj, id)
        return id
    

@dataclass
class DeleteAnswerCommand:
    answer_repo: AnswerRepository
    
    async def __call__(self, id: UUID) -> str:
        await self.answer_repo.delete(id)
        return id
        