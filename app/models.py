from enum import StrEnum

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


"""

Доменные модели

"""


class ChatMessage(BaseModel):
    role: MessageRole
    content: str


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Conversation(BaseModel):
    id: int


"""

HTTP DTO модели

"""


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str = Field(min_length=1)


class ConversationResponse(BaseModel):
    conversation_id: int
    messages: list[ChatMessage]


class ConversationCreated(BaseModel):
    conversation_id: int
