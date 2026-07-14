from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import ConversationSchema, MessageSchema
from sqlalchemy import select
from app.models import MessageRole


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def create_conversation(self) -> ConversationSchema:
        conversation = ConversationSchema()

        self._session.add(conversation)
        self._session.commit()
        self._session.refresh(conversation)

        return conversation

    def get_conversation(self, conversation_id: int) -> ConversationSchema | None:
        statement = select(ConversationSchema).where(
            ConversationSchema.id == conversation_id
        )

        return self._session.scalar(statement)

    def get_messages(self, conversation_id: int) -> list[MessageSchema]:
        statement = (
            select(MessageSchema)
            .where(MessageSchema.conversation_id == conversation_id)
            .order_by(MessageSchema.created_at)
        )

        return list(self._session.scalars(statement))

    def add_message(
        self,
        conversation_id: int,
        role: MessageRole,
        content: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
    ):
        message = MessageSchema(
            conversation_id=conversation_id,
            role=role,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

        self._session.add(message)
        self._session.commit()
        self._session.refresh(message)

        return message

    def get_history_for_llm(self):
        pass
