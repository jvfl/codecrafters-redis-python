from itertools import batched

from app.protocol import BulkStringCodec
from app.storage.key_value import KeyValueStorage
from app.storage.key_value.data_types import StreamData
from app.io import Writer, Reader

from ._command_handler import CommandHandler


STRING_CODEC = BulkStringCodec()


class XAddCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeyValueStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]
        id = args[1]

        data = args[2:]
        value_data = {key: value for (key, value) in batched(data, 2)}

        entry = StreamData(entries={id: value_data})

        await self.keys_storage.store(key, entry)
        await writer.write(STRING_CODEC.encode(id).encode())
