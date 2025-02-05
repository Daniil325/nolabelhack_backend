from uuid import UUID
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.infra.database.reader import AnswerReader
from src.presentation.schemas.answer_schema import AnswerSchema, AnswerSchemaAdd
from src.presentation.schemas.base import ListResponse, ModelResponse
from src.usecases.answers import CreateAnswerCommand, CreateAnswerDto, DeleteAnswerCommand, UpdateAnswerCommand

router = APIRouter(route_class=DishkaRoute)


@router.get(path="/", response_model=ListResponse[AnswerSchema])
async def get_answer_list(reader: FromDishka[AnswerReader]):
    vote_list = await reader.fetch_list()
    return vote_list


@router.get(path="/{id}", response_model=ModelResponse[AnswerSchema])
async def get_answer_by_id(id: str, reader: FromDishka[AnswerReader]):
    items = await reader.fetch_one(id)

    if not items["item"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with ID: {id} not found",
        )

    return items


@router.post(path="/")
async def add_answer(answer: AnswerSchemaAdd, cmd: FromDishka[CreateAnswerCommand]):
    identity = await cmd(
        CreateAnswerDto(
            **answer.model_dump(exclude_unset=True)
        )
    )
    return identity


@router.put(path="/{id}")
async def edit_vote(id: UUID, update: AnswerSchema, cmd: FromDishka[UpdateAnswerCommand]):
    return await cmd(id=id, update_obj=dict(**update.model_dump(exclude_unset=True)))


@router.delete("/{id}")
async def delete_vote(id: UUID, cmd: FromDishka[DeleteAnswerCommand]):
    return await cmd(id)
