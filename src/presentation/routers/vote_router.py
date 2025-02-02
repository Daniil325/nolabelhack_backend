from typing import List
from dishka.integrations.fastapi import (
    FromDishka, inject
)
from fastapi import APIRouter

from src.presentation.schemas.vote_schema import VoteSchema, VoteSchemaAdd
from src.usecases.services.vote_service import VoteService

router = APIRouter()


@router.post(path="/add", response_model=VoteSchema)
@inject
async def add_vote(vote: VoteSchemaAdd, service: FromDishka[VoteService]):
    added_vote = await service.add_vote(vote)

    return added_vote


@router.put("/edit/{id}")
async def edit_vote(id):
    return {"gol": "gol"}


@router.get(path="/list", response_model=List[VoteSchema])
@inject
async def get_vote_list(service: FromDishka[VoteService]):
    vote_list = await service.get_vote_list()
    return vote_list


@router.get("/{id}")
async def view_vote_by_id(id: int):
    return {"gol": True}