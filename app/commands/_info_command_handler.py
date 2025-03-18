from app.io import Writer, Reader
from app.protocol import BulkStringCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler


class InfoCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        subcommand = args[0].upper()

        if subcommand == "REPLICATION":
            await self.handle_replication(writer)

    async def handle_replication(self, writer: Writer) -> None:

        replication_info = ["# Replication"]

        role = "master"
        if self.config.master_info:
            role = "slave"

        replication_info.append(f"role:{role}")

        if role == "master":
            replication_info.append(f"master_replid:{self.config.master_replid}")
            replication_info.append(
                f"master_repl_offset:{self.config.master_repl_offset}"
            )

        response = BulkStringCodec.encode("\r\n".join(replication_info) + "\r\n")
        await writer.write(response)
