from asyncio import StreamWriter

from app.storage.keys import KeysStorage

from ._command_handler import CommandHandler


class SetCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeysStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        key = args[0]
        value = args[1]

        # Handle expiration if PX option is present
        if len(args) > 3 and args[2].lower() == "px":
            try:
                px_value = int(args[3])
                await self.keys_storage.storeWithExpiration(key, value, px_value)
            except (ValueError, IndexError):
                writer.write(b"-ERR Invalid PX value\r\n")
                await writer.drain()
        else:
            await self.keys_storage.store(key, value)

        writer.write(b"+OK\r\n")
        await writer.drain()
