"""

Здесь будут жить все Depends

"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients import OpenAIClient
from app.clients import OllamaClient
from app.database import get_session, get_session_factory
from app.repository import ConversationRepository
from app.services import ChatService
from settings.settings import get_settings
from app.protocols import ConversationRepositoryProtocol, LLMClientProtocol
from app.uow import UnitOfWorkFactory


async def get_repository(
    session: AsyncSession = Depends(get_session),
) -> ConversationRepositoryProtocol:

    return ConversationRepository(session)


def get_llm_client() -> LLMClientProtocol:
    """
    Пример реализации паттерна Factory.
    Создаёт объекты без указания конкретного класса.
    Удобно, когда тип объекта определяется во время выполнения.
    """
    settings = get_settings()

    match settings.LLM_PROVIDER:
        case "ollama":
            return OllamaClient(
                host=settings.OLLAMA_HOST,
                model=settings.LLM_MODEL,
            )

        case "openai":
            return OpenAIClient(
                api_key=settings.OPENAI_API_KEY,
                model=settings.LLM_MODEL,
            )

        case _:
            raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")


def get_uow_factory():

    return UnitOfWorkFactory(
        get_session_factory(),
    )


async def get_chat_service(
    uow_factory=Depends(get_uow_factory),
    client: LLMClientProtocol = Depends(get_llm_client),
) -> ChatService:

    return ChatService(
        uow_factory=uow_factory,
        client=client,
    )
