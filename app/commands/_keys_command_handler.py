import re
from asyncio import StreamWriter
from typing import Any

from app.commands._command_handler import CommandHandler
from app.protocol import ArrayCodec


class KeysCommandHandler(CommandHandler):
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        pattern = args[0]
        expression = re.compile(pattern.replace("*", ".*"))

        keys = self.memory.keys()
        results = [key for key in keys if expression.match(key)]

        response = ArrayCodec().encode(results)
        writer.write(response.encode("utf-8"))
        await writer.drain()
