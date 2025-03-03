import re
from asyncio import StreamWriter

from app.protocol import ArrayCodec
from app.storage.keys import KeysStorage

from ._command_handler import CommandHandler


class KeysCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        pattern = args[0]
        expression = re.compile(pattern.replace("*", ".*"))

        keys = await self.keys_storage.keys()
        results = [key for key in keys if expression.match(key)]

        response = ArrayCodec().encode(results)
        writer.write(response.encode("utf-8"))
        await writer.drain()
