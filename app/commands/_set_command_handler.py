from app.storage.keys import KeysStorage
from app.storage.keys.data_types import StringEntry

from app.io import Writer, Reader

from ._command_handler import CommandHandler


class SetCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]
        value = StringEntry(args[1])

        # Handle expiration if PX option is present
        if len(args) > 3 and args[2].lower() == "px":
            try:
                px_value = int(args[3])
                await self.keys_storage.storeWithExpiration(key, value, px_value)
            except (ValueError, IndexError):
                await writer.write("-ERR Invalid PX value\r\n".encode())
        else:
            await self.keys_storage.store(key, value)

        await writer.write("+OK\r\n".encode())
