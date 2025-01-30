from fastapi import APIRouter

router = APIRouter()


@router.get("/{id}")
async def view_vote_by_id(id):
    return {"gol": True}


@router.post("/add")
async def add_vote():
    return {"gol": True}


@router.put("/edit/{id}")
async def edit_vote(id):
    return {"gol": True}


@router.get("/list")
async def get_vote_list():
    return {"gol_list": True}
