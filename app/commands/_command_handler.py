from abc import ABC, abstractmethod

from app.io import Writer


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, args: list[str], writer: Writer) -> None:
        raise NotImplementedError
