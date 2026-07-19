from __future__ import annotations

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.clients.stream import StreamResult
from app.models import ChatMessage
from app.protocols import LLMClientProtocol


class OllamaStreamResult(StreamResult):
    def __init__(self, response):
        super().__init__()
        self._response = response

    async def stream(self) -> AsyncIterator[str]:

        try:
            async for chunk in self._response:
                if chunk.choices:
                    delta = chunk.choices[0].delta.content

                    if delta:
                        yield delta

            # Ollama через OpenAI-compatible API
            # обычно не возвращает usage.
            self._usage = None

        finally:
            self._finished = True


class OllamaClient(LLMClientProtocol):
    def __init__(
        self,
        host: str,
        model: str,
    ):
        self._model = model

        self._client = AsyncOpenAI(
            base_url=host,
            api_key="ollama",
        )

    async def chat(
        self,
        messages: list[ChatMessage],
    ) -> StreamResult:

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in messages
            ],
            stream=True,
        )

        return OllamaStreamResult(response)
