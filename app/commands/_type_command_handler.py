from app.commands._command_handler import CommandHandler
from app.io import Writer, Reader
from app.protocol import BulkStringCodec
from app.storage.keys import KeysStorage

STRING_CODEC = BulkStringCodec()


class TypeCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]

        value = await self.keys_storage.retrieve(key)

        if value:
            await writer.write("+string\r\n".encode())
        else:
            await writer.write("+none\r\n".encode())
