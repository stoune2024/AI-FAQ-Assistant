"""

Основная бизнес логика приложения

"""

from typing import AsyncIterator

from app.models import MessageRole
from sqlalchemy.ext.asyncio import AsyncSession
from app.protocols import ConversationRepositoryProtocol, LLMClientProtocol


class ChatSession:
    def __init__(
        self,
        conversation_id: int,
        stream: AsyncIterator[str],
    ):
        self.conversation_id = conversation_id
        self._stream = stream

    def stream(self) -> AsyncIterator[str]:
        return self._stream


class ChatService:
    def __init__(
        self,
        session: AsyncSession,
        repository: ConversationRepositoryProtocol,
        client: LLMClientProtocol,
    ):
        self._session = session
        self._repository = repository
        self._client = client

    async def chat(self, conversation_id: int | None, user_message: str) -> ChatSession:
        if conversation_id is None:
            conversation = await self._repository.create_conversation()
            conversation_id = conversation.id

        await self._repository.add_message(
            conversation_id=conversation_id, role=MessageRole.USER, content=user_message
        )

        history = await self._repository.get_history_for_llm(conversation_id)
        if not history:
            raise RuntimeError("Conversation history is empty.")
        print(f"История клиента: {history}")
        result = await self._client.chat(history)

        async def stream():

            chunks = []

            try:
                async for chunk in result.stream():
                    chunks.append(chunk)

                    yield chunk

                await self._repository.add_message(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content="".join(chunks),
                    prompt_tokens=result.usage.prompt_tokens,
                    completion_tokens=result.usage.completion_tokens,
                    total_tokens=result.usage.total_tokens,
                )

                await self._session.commit()
            except Exception:
                await self._session.rollback()
                raise

        return ChatSession(conversation_id=conversation_id, stream=stream())
