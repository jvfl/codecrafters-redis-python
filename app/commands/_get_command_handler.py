from asyncio import StreamWriter

from app.commands._command_handler import CommandHandler
from app.protocol import BulkStringCodec
from app.storage.keys import KeysStorage

STRING_CODEC = BulkStringCodec()


class GetCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        key = args[0]

        value = await self.keys_storage.retrieve(key)

        if value:
            encoded_string = STRING_CODEC.encode(value)
            writer.write(encoded_string.encode("utf-8"))
        else:
            writer.write(b"$-1\r\n")
        await writer.drain()
