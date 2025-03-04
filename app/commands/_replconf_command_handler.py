from app.io import Writer, ConnectionWriter
from app.protocol import ArrayCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

ARRAY_CODEC = ArrayCodec()


class ReplConfCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: Writer) -> None:
        subcommand = args[0].upper()

        if subcommand == "LISTENING-PORT":
            await self.handle_listening_port(int(args[1]), writer)
        elif subcommand == "CAPA":
            await self.handle_capabilities(args[1], writer)
        elif subcommand == "GETACK":
            await self.handle_getack(args[1], writer)

    async def handle_listening_port(
        self, listening_port: int, writer: Writer  # noqa: ARG002
    ) -> None:
        if isinstance(writer, ConnectionWriter):
            self.config.replica_connections.append(writer._connection)
        await writer.write("+OK\r\n".encode())

    async def handle_capabilities(
        self, capabilities: str, writer: Writer  # noqa: ARG002
    ) -> None:
        await writer.write("+OK\r\n".encode())

    async def handle_getack(self, offset: str, writer: Writer) -> None:  # noqa: ARG002
        response = ["REPLCONF", "ACK", str(self.config.master_repl_offset)]

        await writer.write(ARRAY_CODEC.encode(response).encode())
