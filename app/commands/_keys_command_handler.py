import re

from app.io import Writer, Reader
from app.protocol import ArrayCodec
from app.storage.key_value import KeyValueStorage

from ._command_handler import CommandHandler


class KeysCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeyValueStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        pattern = args[0]
        expression = re.compile(pattern.replace("*", ".*"))

        keys = await self.keys_storage.keys()
        results = [key for key in keys if expression.match(key)]

        response = ArrayCodec().encode(results)
        await writer.write(response.encode())
