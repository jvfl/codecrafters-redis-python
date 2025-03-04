from asyncio import StreamWriter

from app.protocol import ArrayCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

ARRAY_CODEC = ArrayCodec()


class ReplConfCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        subcommand = args[0].upper()

        if subcommand == "LISTENING-PORT":
            await self.handle_listening_port(int(args[1]), writer)
        elif subcommand == "CAPA":
            await self.handle_capabilities(args[1], writer)
        elif subcommand == "GETACK":
            await self.handle_getack(args[1], writer)

    async def handle_listening_port(
        self, listening_port: int, writer: StreamWriter  # noqa: ARG002
    ) -> None:
        self.config.replica_connections.append(writer)
        writer.write(b"+OK\r\n")
        await writer.drain()

    async def handle_capabilities(
        self, capabilities: str, writer: StreamWriter  # noqa: ARG002
    ) -> None:
        writer.write(b"+OK\r\n")
        await writer.drain()

    async def handle_getack(
        self, offset: str, writer: StreamWriter  # noqa: ARG002
    ) -> None:
        response = ["REPLCONF", "ACK", "0"]

        writer.write(ARRAY_CODEC.encode(response).encode())
        await writer.drain()
