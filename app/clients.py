"""

Хранение клиентов внешних сервисов, например OpenAIClient

"""

from openai import AsyncOpenAI
from fastapi.responses import StreamingResponse


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(...)

    async def stream_chat(self, messages: list[dict]) -> StreamingResponse:
        pass
