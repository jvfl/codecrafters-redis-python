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

        role = "master"
        if self.config.replicaof:
            role = "slave"

        replication_info = "\r\n".join(["# Replication", f"role:{role}"])

        response = STRING_CODEC.encode(replication_info + "\r\n")
        writer.write(response.encode("utf-8"))
        await writer.drain()
