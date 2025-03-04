from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    async def read(self, bytes_to_read: int) -> bytes:
        raise NotImplementedError
