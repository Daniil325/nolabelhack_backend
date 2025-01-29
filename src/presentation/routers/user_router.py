from fastapi import APIRouter

router = APIRouter()


@router.get("/login")
async def get_user_login_page():
    return {"gol": True}


@router.post("/login")
async def user_login():
    return {"gol": True}


@router.get("/registration")
async def get_user_registration_page():
    return {"gol": True}


@router.post("/registration")
async def user_registration():
    return {"gol": True}


@router.get("/profile")
async def get_user_profile_page():
    #можно сделать через получение объекта юзера и вытягивания его ид
    return {"gol": True}


@router.put("/profile")
async def change_user_profile():
    return {"gol": True}