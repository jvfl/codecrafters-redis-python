import asyncio

from dataclasses import dataclass, field

from app.protocol._array_codec import ArrayCodec

from ._redis_node_info import RedisNodeInfo

ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisSyncManager:
    current_node_info: RedisNodeInfo
    master_info: RedisNodeInfo
    reader: asyncio.StreamReader = field(init=False)
    writer: asyncio.StreamWriter = field(init=False)

    async def sync_with_master(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(
            self.master_info.host, self.master_info.port
        )

        await self._handshake()

    async def _handshake(self) -> None:
        await self._send_command("PING")
        await self._handle_response()

        await self._send_command(
            f"REPLCONF listening-port {self.current_node_info.port}"
        )
        await self._handle_response()

        await self._send_command("REPLCONF capa psync2")
        await self._handle_response()

        await self._send_command("PSYNC ? -1")
        await self._handle_response()

    async def _send_command(self, command: str) -> None:
        encoded_command = ARRAY_CODEC.encode(command.split(" "))

        self.writer.write(encoded_command.encode())
        await self.writer.drain()

    async def _handle_response(self) -> None:
        await self.reader.read(100)
