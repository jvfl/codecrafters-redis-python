from asyncio import StreamWriter
from dataclasses import asdict

from app.protocol import BulkStringCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

STRING_CODEC = BulkStringCodec()


class InfoCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = asdict(config)

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        subcommand = args[0].upper()

        if subcommand == "REPLICATION":
            await self.handle_replication(writer)

    async def handle_replication(self, writer: StreamWriter) -> None:
        response = STRING_CODEC.encode("# Replication\r\nrole:master\r\n")
        writer.write(response.encode("utf-8"))
        await writer.drain()
