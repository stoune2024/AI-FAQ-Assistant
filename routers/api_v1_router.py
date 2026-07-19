from fastapi import APIRouter
from fastapi import FastAPI

from app.controllers import router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(router)

app.include_router(api_router)
