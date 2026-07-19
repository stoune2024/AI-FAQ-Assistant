from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.models import TokenUsage


class StreamResult(ABC):
    """
    Абстрактный результат стриминга LLM.

    После полного завершения stream() свойство usage
    либо содержит TokenUsage, либо None, если провайдер
    не предоставляет статистику токенов.
    """

    def __init__(self) -> None:
        self._usage: TokenUsage | None = None
        self._finished = False

    @property
    def usage(self) -> TokenUsage | None:
        if not self._finished:
            raise RuntimeError("Streaming has not finished yet.")

        return self._usage

    @abstractmethod
    async def stream(self) -> AsyncIterator[str]: ...
