from abc import ABC, abstractmethod

from asyncio import StreamWriter


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        raise NotImplementedError
