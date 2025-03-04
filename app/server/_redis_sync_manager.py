import asyncio

from dataclasses import dataclass

from app.protocol._array_codec import ArrayCodec

from ._redis_node_info import RedisNodeInfo

ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisSyncManager:
    current_node_info: RedisNodeInfo
    master_info: RedisNodeInfo

    async def sync_with_master(self):
        reader, writer = await asyncio.open_connection(
            self.master_info.host, self.master_info.port
        )

        await self._handshake(reader, writer)

    async def _handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ):

        writer.write(ARRAY_CODEC.encode(["PING"]).encode())
        await writer.drain()

        await reader.read(100)

        writer.write(
            ARRAY_CODEC.encode(
                ["REPLCONF", "listening-port", str(self.current_node_info.port)]
            ).encode()
        )
        await writer.drain()

        await reader.read(100)

        writer.write(ARRAY_CODEC.encode(["REPLCONF", "capa", "psync2"]).encode())
        await writer.drain()
