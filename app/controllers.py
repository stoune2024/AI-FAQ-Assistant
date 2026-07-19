from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_chat_service
from app.models import ChatRequest
from app.services import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):

    result = await service.chat(
        conversation_id=request.conversation_id,
        user_message=request.message,
    )

    headers = {"X-Conversation-ID": str(result.conversation_id)}

    return StreamingResponse(
        result.stream(),
        media_type="text/plain",
        headers=headers,
    )
