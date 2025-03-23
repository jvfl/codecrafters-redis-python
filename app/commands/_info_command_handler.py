from app.io import ConnectionManager
from app.protocol import Resp2Data, BulkString

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("INFO")
class InfoCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        subcommand = args[0].upper()

        if subcommand == "REPLICATION":
            return await self.handle_replication()

        return BulkString(None)

    async def handle_replication(self) -> Resp2Data:
        replication_info = ["# Replication"]

        role = "master"
        if self._config.master_info:
            role = "slave"

        replication_info.append(f"role:{role}")

        if role == "master":
            replication_info.append(f"master_replid:{self._config.master_replid}")
            replication_info.append(
                f"master_repl_offset:{self._config.master_repl_offset}"
            )

        return BulkString("\r\n".join(replication_info) + "\r\n")
