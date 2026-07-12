import uvicorn
from routers.api_v1_router import app
from settings.settings import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
