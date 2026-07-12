from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import ConversationSchema, MessageSchema


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def create_conversation(self) -> ConversationSchema:
        pass

    def get_conversation(self, conversation_id: int) -> ConversationSchema | None:
        pass

    def get_messages(self, conversation_id: int) -> list[MessageSchema]:
        pass

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
    ):
        pass

    def get_history_for_llm(self):
        pass
