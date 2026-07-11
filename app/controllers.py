from fastapi import APIRouter

router = APIRouter(tags=["Роутер сервиса"])


@router.get("/")
async def get_hw_page():
    return {"message": "Привет из ручки сервиса!"}
