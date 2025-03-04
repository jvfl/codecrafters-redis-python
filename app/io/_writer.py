from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    async def write(self, message: bytes) -> None:
        raise NotImplementedError
