from fastapi import FastAPI
from src.presentation.routers import api_router
from dishka.integrations.fastapi import setup_dishka
from src.infra.di import container


def create_app():
    app: FastAPI = FastAPI()
    app.include_router(api_router)

    setup_dishka(container, app)

    return app
