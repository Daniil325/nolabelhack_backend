from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from src.infra.database.reader import VoteReader
from src.presentation.schemas.base import ListResponse, ModelResponse
from src.presentation.schemas.vote_schema import VoteSchema, VoteSchemaAdd
from src.usecases.vote import (
    CreateVoteCommand,
    CreateVoteDto,
    DeleteVoteCommand,
    UpdateVoteCommand,
)

router = APIRouter(route_class=DishkaRoute)


@router.get(path="/", response_model=ListResponse[VoteSchema])
async def get_vote_list(reader: FromDishka[VoteReader]):
    vote_list = await reader.fetch_list()
    return vote_list


@router.get(path="/{id}", response_model=ModelResponse[VoteSchema])
async def get_vote_by_id(id: str, reader: FromDishka[VoteReader]):
    return await reader.fetch_one(id)


@router.post(path="/")
async def add_vote(vote: VoteSchemaAdd, cmd: FromDishka[CreateVoteCommand]):
    identity = await cmd(
        CreateVoteDto(
            **vote.model_dump(exclude_unset=True),
        )
    )
    return identity


@router.put("/{id}")
async def edit_vote(id: str, update: VoteSchema, cmd: FromDishka[UpdateVoteCommand]):
    return await cmd(id=id, update_obj=dict(**update.model_dump(exclude_unset=True)))


@router.delete("/{id}")
async def delete_vote(id: str, cmd: FromDishka[DeleteVoteCommand]):
    return await cmd(id)
