from asyncio import StreamWriter
from dataclasses import dataclass

from ._writer import Writer


@dataclass
class ConnectionWriter(Writer):
    connection: StreamWriter

    async def write(self, message: bytes) -> None:
        self.connection.write(message)
        await self.connection.drain()
