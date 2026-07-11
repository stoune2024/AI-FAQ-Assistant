from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.settings import settings

engine = create_async_engine(settings.db_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[Any, Depends(get_session)]


class Repository:
    """
    Класс для взаимодействия с БД
    """

    @staticmethod
    async def get_by_idempotency_key(session, key):
        pass
