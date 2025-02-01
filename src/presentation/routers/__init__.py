from fastapi import APIRouter

from .index_router import router as index_router
from .user_router import router as user_router
from .vote_router import router as vote_router

api_router = APIRouter()
api_router.include_router(index_router, tags=["Index"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(vote_router, prefix="/vote", tags=["Vote"])
