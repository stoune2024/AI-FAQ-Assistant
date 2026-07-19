"""

Здесь будут жить все Depends

"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients import OpenAIClient
from app.database import get_session
from app.repository import ConversationRepository
from app.services import ChatService
from settings.settings import get_settings
from app.protocols import ConversationRepositoryProtocol, LLMClientProtocol


async def get_repository(
    session: AsyncSession = Depends(get_session),
) -> ConversationRepositoryProtocol:

    return ConversationRepository(session)


def get_llm_client() -> LLMClientProtocol:

    settings = get_settings()

    return OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )


async def get_chat_service(
    session: AsyncSession = Depends(get_session),
    repository: ConversationRepository = Depends(get_repository),
    client: OpenAIClient = Depends(get_llm_client),
) -> ChatService:

    return ChatService(
        session=session,
        repository=repository,
        client=client,
    )
