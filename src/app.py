from fastapi import FastAPI
from src.presentation.routers import api_router
from dishka.integrations.fastapi import setup_dishka
from starlette.middleware.cors import CORSMiddleware
from src.infra.di import container


def create_app():
    app: FastAPI = FastAPI()
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_dishka(container, app)

    return app
