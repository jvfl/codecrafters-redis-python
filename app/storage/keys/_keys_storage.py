from abc import ABC, abstractmethod
from typing import Optional

from .data_types import DataEntry


class KeysStorage(ABC):
    @abstractmethod
    async def store(self, key: str, value: DataEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    async def storeWithExpiration(
        self, key: str, value: DataEntry, expire_in_millis: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[DataEntry]:
        raise NotImplementedError

    @abstractmethod
    async def keys(self) -> list[str]:
        raise NotImplementedError
