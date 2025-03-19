import time

from itertools import batched
from typing import Optional, Tuple, cast

from app.protocol import BulkStringCodec
from app.storage.key_value.data_types import StreamData, StreamDataEntry
from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory

MIN_ID_ERROR_MSG = "-ERR The ID specified in XADD must be greater than 0-0\r\n"
SHOULD_BE_BIGGER_ERROR_MSG = (
    "-ERR The ID specified in XADD is equal or smaller than"
    " the target stream top item\r\n"
)


@CommandHandlerFactory.register("XADD")
class XAddCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]
        stream = await self._retrieve_stream(key)

        id = args[1]
        millis, seq_number = self._process_id(id, stream)

        if error := self._validate_id(stream, millis, seq_number):
            await writer.write(error.encode())
            return

        stream_data = args[2:]
        value_data = {key: value for (key, value) in batched(stream_data, 2)}
        stream.entries.append(StreamDataEntry(millis, seq_number, value_data))

        await self._keys_storage.store(key, stream)
        await writer.write(BulkStringCodec.encode(f"{millis}-{seq_number}"))

    def _process_id(self, id: str, stream: StreamData) -> Tuple[int, int]:
        if id == "*":
            millis = time.time_ns() // 1_000_000
            seq_number = self._generate_seq_number(stream, millis)
            return (millis, seq_number)

        raw_millis, raw_seq_number = id.split("-")

        millis = int(raw_millis)
        seq_number = (
            int(raw_seq_number)
            if raw_seq_number != "*"
            else self._generate_seq_number(stream, millis)
        )

        return (millis, seq_number)

    def _generate_seq_number(self, stream: StreamData, millis: int) -> int:
        seq_numbers = [
            entry.seq_number for entry in stream.entries if entry.millis == millis
        ]

        if len(seq_numbers) == 0:
            if millis == 0:
                return 1
            else:
                return 0
        else:
            last_seq_number = max(seq_numbers)
            return last_seq_number + 1

    async def _retrieve_stream(self, key: str) -> StreamData:
        data = await self._keys_storage.retrieve(key)

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
