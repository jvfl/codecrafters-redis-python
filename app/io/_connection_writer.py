from asyncio import StreamWriter

from ._writer import Writer


class ConnectionWriter(Writer):
    def __init__(self, connection: StreamWriter):
        self._connection = connection

    async def write(self, message: bytes) -> None:
        self._connection.write(message)
        await self._connection.drain()
