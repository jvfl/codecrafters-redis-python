import asyncio

from typing import Optional

from ._keys_storage import KeysStorage


class InMemoryKeysStorage(KeysStorage):
    def __init__(self):
        self.hash_table = {}

    async def store(self, key: str, value: str) -> None:
        self.hash_table[key] = value

    async def storeWithExpiration(
        self, key: str, value: str, expire_in_millis: int
    ) -> None:
        await self.store(key, value)
        asyncio.create_task(self._expire_key(key, expire_in_millis))

    async def _expire_key(self, key: str, delay_ms: int) -> None:
        await asyncio.sleep(delay_ms / 1000.0)  # Convert ms to seconds
        self.hash_table.pop(key, None)

    async def retrieve(self, key: str) -> Optional[str]:
        value = self.hash_table.get(key, None)
        return value

    async def keys(self) -> list[str]:
        return self.hash_table.keys()
