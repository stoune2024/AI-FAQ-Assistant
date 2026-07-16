"""

Основная бизнес логика приложения

"""

from typing import AsyncIterator

from app.repository import ConversationRepository
from app.clients import OpenAIClient
from app.models import MessageRole, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession


class ChatResult:
    def __init__(
        self,
        conversation_id: int,
        stream: AsyncIterator[str],
    ):
        self.conversation_id = conversation_id
        self.stream = stream


class ChatService:
    def __init__(
        self,
        session: AsyncSession,
        repository: ConversationRepository,
        client: OpenAIClient,
    ):
        self._session = session
        self._repository = repository
        self._client = client

    async def chat(self, conversation_id: int | None, user_message: str) -> ChatResult:
        if conversation_id is None:
            conversation = await self._repository.create_conversation()
            conversation_id = conversation.id

        self._repository.add_message(
            conversation_id=conversation_id, role=MessageRole.USER, content=user_message
        )

        history = [
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in self._repository.get_messages(conversation_id)
        ]

        result = await self._client.chat(history)

        async def stream():

            chunks = []

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

        return ChatResult(conversation_id=conversation_id, stream=stream())
