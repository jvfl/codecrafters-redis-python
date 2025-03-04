import asyncio

from dataclasses import dataclass, field

from app.protocol._array_codec import ArrayCodec
from app.commands import CommandHandlerFactory

from ._redis_node_info import RedisNodeInfo

ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisSyncManager:
    current_node_info: RedisNodeInfo
    master_info: RedisNodeInfo
    command_factory: CommandHandlerFactory
    reader: asyncio.StreamReader = field(init=False)
    writer: asyncio.StreamWriter = field(init=False)

    async def sync_with_master(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(
            self.master_info.host, self.master_info.port
        )

        await self._handshake()
        await self._ask_for_rdb()

        asyncio.create_task(self._process_master_commands())

    async def _handshake(self) -> None:
        await self._send_command("PING")
        await self._handle_response()

        await self._send_command(
            f"REPLCONF listening-port {self.current_node_info.port}"
        )
        await self._handle_response()

        await self._send_command("REPLCONF capa psync2")
        await self._handle_response()

    async def _ask_for_rdb(self) -> None:
        await self._send_command("PSYNC ? -1")
        await self._handle_response()
        await self._handle_response()

    async def _process_master_commands(self) -> None:
        while True:
            print("Replica listening...")
            command_bytes = await self.reader.read(100)
            raw_commands = command_bytes.decode()

            print("Raw commands", raw_commands)

            if raw_commands == "":
                break

            for raw_command in raw_commands.split("\r\n*"):
                if not raw_command.startswith("*"):
                    raw_command = f"*{raw_command}"

                commandAndArgs = ARRAY_CODEC.decode(raw_command + "\r\n")
                print("Replica Command:", commandAndArgs)
                command = commandAndArgs[0].upper()
                args = commandAndArgs[1:]

                await self.command_factory.create(command).handle(args, self.writer)

    async def _send_command(self, command: str) -> None:
        encoded_command = ARRAY_CODEC.encode(command.split(" "))

        self.writer.write(encoded_command.encode())
        await self.writer.drain()

    async def _handle_response(self) -> None:
        await self.reader.read(100)
