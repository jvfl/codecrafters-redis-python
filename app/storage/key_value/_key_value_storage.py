from abc import ABC, abstractmethod
from typing import Optional

from .data_types import Data


class KeyValueStorage(ABC):
    @abstractmethod
    async def store(self, key: str, value: Data) -> None:
        raise NotImplementedError

    @abstractmethod
    async def storeWithExpiration(
        self, key: str, value: Data, expire_in_millis: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Data]:
        raise NotImplementedError

    @abstractmethod
    async def keys(self) -> list[str]:
        raise NotImplementedError
