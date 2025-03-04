import asyncio

from dataclasses import dataclass, field

from app.protocol._array_codec import ArrayCodec
from app.commands import CommandHandlerFactory
from app.io import ConnectionWriter, NoOpWriter, Writer, ConnectionReader

from ._redis_config import RedisConfig
from ._redis_node_info import RedisNodeInfo

ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisSyncManager:
    current_node_info: RedisNodeInfo
    master_info: RedisNodeInfo
    command_factory: CommandHandlerFactory
    config: RedisConfig
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
        await self._handle_response(7)

        await self._send_command(
            f"REPLCONF listening-port {self.current_node_info.port}"
        )
        await self._handle_response(5)

        await self._send_command("REPLCONF capa psync2")
        await self._handle_response(5)

    async def _ask_for_rdb(self) -> None:
        await self._send_command("PSYNC ? -1")
        await self._handle_response(56)
        await self._handle_response(93)

    async def _process_master_commands(self) -> None:
        while True:
            print("Replica listening...")
            command_bytes = await self.reader.read(1024)
            raw_commands = command_bytes.decode()

            print("Raw commands", raw_commands)

            if raw_commands == "":
                break

            commands = []
            while raw_commands != "":
                commandAndArgs = ARRAY_CODEC.decode(raw_commands)
                commands.append(commandAndArgs)
                raw_commands = raw_commands.replace(
                    ARRAY_CODEC.encode(commandAndArgs), ""
                )

            for commandAndArgs in commands:
                print("Replica Command:", commandAndArgs)
                command = commandAndArgs[0].upper()
                args = commandAndArgs[1:]

                handler = self.command_factory.create(command)

                writer: Writer = NoOpWriter()
                if command == "REPLCONF":
                    writer = ConnectionWriter(self.writer)

                await handler.handle(args, writer, ConnectionReader(self.reader))
                self.config.replica_offset += len(
                    ARRAY_CODEC.encode(commandAndArgs).encode()
                )

    async def _send_command(self, command: str) -> None:
        print("Sending command", command)
        encoded_command = ARRAY_CODEC.encode(command.split(" "))

        self.writer.write(encoded_command.encode())
        await self.writer.drain()

    async def _handle_response(self, bytes_to_read: int) -> None:
        response = await self.reader.read(bytes_to_read)
        print("Handled response", response.decode(errors="replace"))
        print("Response end")
        print()
