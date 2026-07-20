"""

Основная бизнес логика приложения

"""

from typing import AsyncIterator

from app.models import MessageRole
from app.protocols import (
    LLMClientProtocol,
    UnitOfWorkFactoryProtocol,
)


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
        uow_factory: UnitOfWorkFactoryProtocol,
        client: LLMClientProtocol,
    ):
        self._uow_factory = uow_factory
        self._client = client

    async def chat(self, conversation_id: int | None, user_message: str) -> ChatSession:
        # 1. Создание разговора
        if conversation_id is None:
            async with self._uow_factory() as uow:
                conversation = await uow.conversations.create_conversation()
                await uow.commit()
                conversation_id = conversation.id

        # 2. Сохранение пользовательского сообщения
        async with self._uow_factory() as uow:
            await uow.conversations.add_message(
                conversation_id=conversation_id,
                role=MessageRole.USER,
                content=user_message,
            )
            await uow.commit()

        # 3. Получение истории
        async with self._uow_factory() as uow:
            history = await uow.conversations.get_history_for_llm(conversation_id)
            if not history:
                raise RuntimeError("Conversation history is empty.")

        result = await self._client.chat(history)

        async def stream():

            chunks = []

            async for chunk in result.stream():
                chunks.append(chunk)

                yield chunk
            # 4. Создание сообщения ассистента
            async with self._uow_factory() as uow:
                usage = result.usage

                await uow.conversations.add_message(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content="".join(chunks),
                    prompt_tokens=usage.prompt_tokens if usage else None,
                    completion_tokens=usage.completion_tokens if usage else None,
                    total_tokens=usage.total_tokens if usage else None,
                )

                await uow.commit()

        return ChatSession(conversation_id=conversation_id, stream=stream())
