from asyncio import StreamWriter

from app.protocol import BulkStringCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

STRING_CODEC = BulkStringCodec()


class InfoCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        subcommand = args[0].upper()

        if subcommand == "REPLICATION":
            await self.handle_replication(writer)

    async def handle_replication(self, writer: StreamWriter) -> None:

        replication_info = ["# Replication"]

        role = "master"
        if self.config.replicaof:
            role = "slave"

        replication_info.append(f"role:{role}")

        if role == "master":
            replication_info.append(f"master_replid:{self.config.master_replid}")
            replication_info.append(
                f"master_repl_offset:{self.config.master_repl_offset}"
            )

        response = STRING_CODEC.encode("\r\n".join(replication_info) + "\r\n")
        writer.write(response.encode("utf-8"))
        await writer.drain()
