import asyncio

from typing import Optional

from .data_types import Data
from ._key_value_storage import KeyValueStorage


class InMemoryStorage(KeyValueStorage):
    def __init__(self) -> None:
        self.hash_table: dict[str, Data] = {}

    async def store(self, key: str, value: Data) -> None:
        self.hash_table[key] = value

    async def storeWithExpiration(
        self, key: str, value: Data, expire_in_millis: int
    ) -> None:
        await self.store(key, value)
        asyncio.create_task(self._expire_key(key, expire_in_millis))

    async def _expire_key(self, key: str, delay_ms: int) -> None:
        await asyncio.sleep(delay_ms / 1000.0)  # Convert ms to seconds
        self.hash_table.pop(key, None)

    async def retrieve(self, key: str) -> Optional[Data]:
        value = self.hash_table.get(key, None)
        return value

    async def keys(self) -> list[str]:
        return list(self.hash_table.keys())

    def __repr__(self) -> str:
        return str(self.hash_table)
