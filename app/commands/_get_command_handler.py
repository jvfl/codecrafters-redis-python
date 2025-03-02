from app.commands._command_handler import CommandHandler
from asyncio import StreamWriter
from typing import Any
from app.protocol import BulkStringCodec


STRING_CODEC = BulkStringCodec()


class GetCommandHandler(CommandHandler):
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        key = args[0]

        if value := self.memory.get(key):
            encoded_string = STRING_CODEC.encode(value)
            writer.write(encoded_string.encode("utf-8"))
        else:
            writer.write(b"$-1\r\n")
        await writer.drain()
