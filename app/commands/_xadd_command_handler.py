from itertools import batched
from typing import Optional, cast

from app.protocol import BulkStringCodec
from app.storage.key_value import KeyValueStorage
from app.storage.key_value.data_types import StreamData, StreamDataEntry
from app.io import Writer, Reader

from ._command_handler import CommandHandler


STRING_CODEC = BulkStringCodec()
MIN_ID_ERROR_MSG = "-ERR The ID specified in XADD must be greater than 0-0\r\n"
SHOULD_BE_BIGGER_ERROR_MSG = (
    "-ERR The ID specified in XADD is equal or smaller than"
    " the target stream top item\r\n"
)


class XAddCommandHandler(CommandHandler):
    def __init__(self, keys_storage: KeyValueStorage):
        self.keys_storage = keys_storage

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]
        id = args[1]
        millis, seq_number = (int(part) for part in id.split("-"))

        stream = await self._retrieve_stream(key)

        if error := self._validate_id(stream, millis, seq_number):
            await writer.write(error.encode())
            return

        stream_data = args[2:]
        value_data = {key: value for (key, value) in batched(stream_data, 2)}
        stream.entries.append(StreamDataEntry(millis, seq_number, value_data))

        await self.keys_storage.store(key, stream)
        await writer.write(STRING_CODEC.encode(id).encode())

    async def _retrieve_stream(self, key: str) -> StreamData:
        data = await self.keys_storage.retrieve(key)

        has_no_data_stream = data is None or not isinstance(data, StreamData)

        current_stream = StreamData([])
        if not has_no_data_stream:
            current_stream = cast(StreamData, data)

        return current_stream

    def _validate_id(
        self, stream: StreamData, millis: int, seq_number: int
    ) -> Optional[str]:
        if millis <= 0 and seq_number <= 0:
            return MIN_ID_ERROR_MSG

        if len(stream.entries) > 0:
            last_entry = stream.entries[-1]
            is_valid_id = last_entry.millis < millis or (
                last_entry.millis == millis and last_entry.seq_number < seq_number
            )

            if not is_valid_id:
                return SHOULD_BE_BIGGER_ERROR_MSG

        return None
