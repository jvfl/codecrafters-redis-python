from abc import ABC, abstractmethod

from app.io import Writer, Reader


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, args: list[str], writer: Writer, reader: Reader) -> None:
        raise NotImplementedError
