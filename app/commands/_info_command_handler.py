from app.commands._command_handler import CommandHandler
from asyncio import StreamWriter
from typing import Any

from app.protocol import BulkStringCodec, ArrayCodec

STRING_CODEC = BulkStringCodec()
ARRAY_CODEC = ArrayCodec()


class InfoCommandHandler(CommandHandler):
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        subcommand = args[0].upper()

        if subcommand == "REPLICATION":
            await self.handle_replication(writer)

    async def handle_replication(self, writer: StreamWriter) -> None:
        response = STRING_CODEC.encode("# Replication\r\nrole:master\r\n")
        writer.write(response.encode("utf-8"))
        await writer.drain()
