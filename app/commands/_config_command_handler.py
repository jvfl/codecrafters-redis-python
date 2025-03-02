from app.commands._command_handler import CommandHandler
from asyncio import StreamWriter
from typing import Any

from app.protocol import BulkStringCodec, ArrayCodec

STRING_CODEC = BulkStringCodec()
ARRAY_CODEC = ArrayCodec()


class ConfigCommandHandler(CommandHandler):
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        subcommand = args[0]

        if subcommand == "GET":
            await self.handle_get(args[1:], writer)

    async def handle_get(self, args: list[str], writer: StreamWriter) -> None:
        config_key = args[0]

        response = ARRAY_CODEC.encode([config_key, self.memory[config_key]])
        writer.write(response.encode("utf-8"))
        await writer.drain()
