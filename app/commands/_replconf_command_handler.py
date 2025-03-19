from app.protocol import ArrayCodec
from app.server import ReplicaConnection
from app.io import Writer, ConnectionWriter, Reader, ConnectionReader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("REPLCONF")
class ReplConfCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, reader: Reader) -> None:
        subcommand = args[0].upper()

        if subcommand == "LISTENING-PORT":
            await self.handle_listening_port(int(args[1]), writer, reader)
        elif subcommand == "CAPA":
            await self.handle_capabilities(args[1], writer)
        elif subcommand == "GETACK":
            await self.handle_getack(args[1], writer)

    async def handle_listening_port(
        self, listening_port: int, writer: Writer, reader: Reader  # noqa: ARG002
    ) -> None:
        if isinstance(writer, ConnectionWriter) and isinstance(
            reader, ConnectionReader
        ):
            connection = ReplicaConnection(writer, reader)
            self._config.replica_connections.append(connection)
        await writer.write("+OK\r\n".encode())

    async def handle_capabilities(
        self, capabilities: str, writer: Writer  # noqa: ARG002
    ) -> None:
        await writer.write("+OK\r\n".encode())

    async def handle_getack(self, offset: str, writer: Writer) -> None:  # noqa: ARG002
        response = ["REPLCONF", "ACK", str(self._config.replica_offset)]

        await writer.write(ArrayCodec.encode(response))
