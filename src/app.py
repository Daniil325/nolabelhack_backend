from fastapi import FastAPI
from src.presentation.routers import index_router
from src.presentation.routers import user_router
from src.presentation.routers import vote_router

app = FastAPI()


app.include_router(index_router.router)
app.include_router(user_router.router, prefix="/user")
app.include_router(vote_router.router, prefix="/vote")
