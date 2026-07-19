from __future__ import annotations

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.clients.stream import StreamResult
from app.models import ChatMessage
from app.models import TokenUsage
from app.protocols import LLMClientProtocol


class OpenAIStreamResult(StreamResult):
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

                if getattr(chunk, "usage", None):
                    self._usage = TokenUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                    )

        finally:
            self._finished = True


class OpenAIClient(LLMClientProtocol):
    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self._model = model

        self._client = AsyncOpenAI(
            api_key=api_key,
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
            stream_options={
                "include_usage": True,
            },
        )

        return OpenAIStreamResult(response)
