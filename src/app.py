from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()


@router.get("/")
async def get_exapmle():
    return {"gooool": "example"}


app.include_router(router)
