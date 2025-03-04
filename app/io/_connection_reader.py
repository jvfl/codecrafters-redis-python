from asyncio import StreamReader
from dataclasses import dataclass

from ._reader import Reader


@dataclass
class ConnectionReader(Reader):
    connection: StreamReader

    async def read(self, bytes_to_read: int) -> bytes:
        return await self.connection.read(bytes_to_read)
