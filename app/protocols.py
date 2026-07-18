from typing import Protocol

from app.clients import StreamResult
from app.models import ChatMessage
from app.models import MessageRole, Conversation
from app.schemas import MessageSchema


class ConversationRepositoryProtocol(Protocol):
    async def create_conversation(
        self,
    ) -> Conversation: ...

    async def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation | None: ...

    async def get_messages(
        self,
        conversation_id: int,
    ) -> list[ChatMessage]: ...

    async def add_message(
        self,
        conversation_id: int,
        role: MessageRole,
        content: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
    ) -> MessageSchema: ...


class LLMClientProtocol(Protocol):
    async def chat(
        self,
        messages: list[ChatMessage],
    ) -> StreamResult: ...
