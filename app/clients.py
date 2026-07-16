"""

Хранение клиентов внешних сервисов, например OpenAIClient

"""

from openai import AsyncOpenAI
from app.models import ChatMessage, TokenUsage
from collections.abc import AsyncIterator


class StreamResult:
    def __init__(
        self,
        response,
    ):
        self._response = response
        self._usage: TokenUsage | None = None

    @property
    def usage(self) -> TokenUsage:

        if self._usage is None:
            raise RuntimeError("Streaming has not finished yet.")

        return self._usage

    async def stream(self) -> AsyncIterator[str]:

        async for chunk in self._response:
            if chunk.choices:
                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

            if chunk.usage:
                self._usage = TokenUsage(
                    prompt_tokens=chunk.usage.prompt_tokens,
                    completion_tokens=chunk.usage.completion_tokens,
                    total_tokens=chunk.usage.total_tokens,
                )


class OpenAIClient:
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

        return StreamResult(response)
