from app.protocol import Resp2Data, BulkString, SimpleString, Array
from app.server import ReplicaConnection
from app.io import ConnectionWriter, ConnectionReader, ConnectionManager

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("REPLCONF")
class ReplConfCommandHandler(CommandHandler):
    async def handle(self, args: list[str], connection: ConnectionManager) -> Resp2Data:
        subcommand = args[0].upper()

        if subcommand == "LISTENING-PORT":
            return await self.handle_listening_port(int(args[1]), connection)
        elif subcommand == "CAPA":
            return await self.handle_capabilities(args[1])
        elif subcommand == "GETACK":
            return await self.handle_getack(args[1])

        return BulkString(None)

    async def handle_listening_port(
        self, listening_port: int, connection: ConnectionManager  # noqa: ARG002
    ) -> Resp2Data:
        if isinstance(connection.writer, ConnectionWriter) and isinstance(
            connection.reader, ConnectionReader
        ):
            replica_conn = ReplicaConnection(connection.writer, connection.reader)
            self._config.replica_connections.append(replica_conn)
        return SimpleString.OK()

    async def handle_capabilities(self, capabilities: str) -> Resp2Data:  # noqa: ARG002
        return SimpleString.OK()

    async def handle_getack(self, offset: str) -> Resp2Data:  # noqa: ARG002
        response = ["REPLCONF", "ACK", str(self._config.replica_offset)]

        return Array(response)
