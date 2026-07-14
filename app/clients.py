"""

Хранение клиентов внешних сервисов, например OpenAIClient

"""

from openai import AsyncOpenAI
from app.models import ChatMessage, TokenUsage
from collections.abc import AsyncGenerator


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)

    async def stream_chat(
        self, messages: list[ChatMessage]
    ) -> AsyncGenerator[str, None]:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            stream=True,
            stream_options={
                "include_usage": True,
            },
        )

        async for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

    async def get_usage(self, messages: list[ChatMessage]) -> TokenUsage:
        """

        Пока заглушка.

        Позже мы объединим stream и usage в одном объекте

        """
        pass
        # return TokenUsage()
