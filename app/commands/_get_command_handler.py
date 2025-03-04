from app.commands._command_handler import CommandHandler
from app.io import Writer, Reader
from app.protocol import BulkStringCodec
from app.storage.keys import KeysStorage

STRING_CODEC = BulkStringCodec()


class GetCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]

        value = await self.keys_storage.retrieve(key)

        if value:
            await writer.write(value.encode())
        else:
            await writer.write("$-1\r\n".encode())
