from dishka import make_async_container
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from src.infra.di.repositories.answer_repository import AnswerRepositoryFactory
from src.infra.di.reader import ReaderProvider
from src.infra.di.database_factory import DatabaseFactory
from src.infra.di.repositories.vote_repository_factory import VoteRepositoryFactory
from src.presentation.routers import api_router
from src.usecases import CommandProvider

def build_container():
    return make_async_container(
        DatabaseFactory(),
        CommandProvider(),
        VoteRepositoryFactory(),
        AnswerRepositoryFactory(),
        ReaderProvider()
    )


def create_app():
    app: FastAPI = FastAPI()
    app.include_router(api_router)
    container = build_container()

    setup_dishka(container, app)

    return app
