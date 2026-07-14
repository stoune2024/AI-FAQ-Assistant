"""

Основная бизнес логика приложения

"""

from app.repository import ConversationRepository
from app.clients import OpenAIClient
from collections.abc import AsyncGenerator
from app.models import MessageRole, ChatMessage


class ChatService:
    def __init__(self, repository: ConversationRepository, client: OpenAIClient):
        self._repository = repository
        self._client = client

    async def chat(
        self, conversation_id: int | None, user_message: str
    ) -> tuple[int, AsyncGenerator[str, None]]:
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

        async def stream():

            answer = []

            async for chunk in self._client.stream_chat(history):
                answer.append(chunk)

                yield chunk

            self._repository.add_message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content="".join(answer),
            )

        return conversation_id, stream()
