from abc import ABC, abstractmethod
from typing import Optional


class KeysStorage(ABC):
    @abstractmethod
    async def store(self, key: str, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def storeWithExpiration(
        self, key: str, value: str, expire_in_millis: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def keys(self) -> list[str]:
        raise NotImplementedError
