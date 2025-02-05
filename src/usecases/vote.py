from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from src.infra.database.models.vote import Vote
from src.infra.database.repository.vote_repository import VoteRepository


@dataclass
class CreateVoteDto:
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    created_at: datetime = datetime.now().replace(tzinfo=None)


@dataclass
class CreateVoteCommand:
    vote_repo: VoteRepository
    # s3_storage: S3ImageStorage

    async def __call__(self, dto: CreateVoteDto) -> str:
        identity = self.vote_repo.new_id()
        vote = Vote(
            id=identity,
            title=dto.title,
            description=dto.description,
            start_date=dto.start_date,
            end_date=dto.end_date,
            is_active=dto.is_active,
            created_at=dto.created_at,
        )
        await self.vote_repo.create(vote)
        return identity


@dataclass
class UpdateVoteCommand:
    vote_repo: VoteRepository

    async def __call__(self, id: UUID, update_obj: dict[str, Any]) -> str:
        await self.vote_repo.update(update_obj, id)
        return id


@dataclass
class DeleteVoteCommand:
    vote_repo: VoteRepository

    async def __call__(self, id: UUID) -> str:
        await self.vote_repo.delete(id)
        return id
