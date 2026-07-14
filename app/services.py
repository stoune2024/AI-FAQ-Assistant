"""

Основная бизнес логика приложения

"""

from typing import AsyncIterator

from app.repository import ConversationRepository
from app.clients import OpenAIClient


class ChatService:
    def __init__(self, repository: ConversationRepository, client: OpenAIClient):
        pass

    def chat(self, conversation_id, user_message) -> AsyncIterator[str]:
        # answer = []
        # answer.append(chunk)
        # yield chunk
        pass
