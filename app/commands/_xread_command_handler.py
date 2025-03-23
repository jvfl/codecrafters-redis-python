import asyncio
import math

from typing import Any

from app.protocol import ArrayCodec, BulkStringCodec
from app.storage.key_value.data_types import StreamData, StreamDataEntry
from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory

WRONGTYPE_ERROR_MSG = (
    "-ERR WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
)


@CommandHandlerFactory.register("XREAD")
class XReadCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        options = args[0]

        stream_refs_start = 1
        block_timeout = 0.0
        check_interval = 100.0
        if options == "block":
            block_timeout = int(args[1]) / 1000.0
            check_interval = block_timeout / 10
            stream_refs_start = 3

        stream_refs = args[stream_refs_start:]
        midpoint = len(stream_refs) // 2
        keys = stream_refs[0:midpoint]
        ids = stream_refs[midpoint:]

        latest_ids: dict[str, str] = {}
        response = await self._read_keys(writer, keys, ids, latest_ids)

        if options == "block" and len(response) == 0:
            if block_timeout == 0.0:
                block_timeout = math.inf

            try:
                async with asyncio.timeout(block_timeout):
                    while len(response) == 0:
                        response = await self._read_keys(writer, keys, ids, latest_ids)
                        await asyncio.sleep(check_interval)
            except asyncio.TimeoutError:
                await writer.write(BulkStringCodec.encode(data=None))
                return

        await writer.write(ArrayCodec.encode(response))

    async def _read_keys(
        self,
        writer: Writer,
        keys: list[str],
        ids: list[str],
        latest_ids: dict[str, str],
    ) -> list[Any]:
        response = []
        for key, start in zip(keys, ids):
            data = await self._keys_storage.retrieve(key)

            if data is None:
                return []

            if not isinstance(data, StreamData):
                await writer.write(WRONGTYPE_ERROR_MSG.encode())
                raise ValueError()

            if start == "$":
                if latest_ids.get(key) is None:
                    latest_ids[key] = data.entries[-1].formatted_id()

                start = latest_ids[key]

            entries = [entry for entry in data.entries if self.in_range(entry, start)]
            if len(entries) > 0:
                response.append(
                    [
                        key,
                        [entry.to_list() for entry in entries],
                    ]
                )

        return response

    def in_range(self, entry: StreamDataEntry, start: str) -> bool:
        start_millis, start_seq_number = [int(raw) for raw in start.split("-")]

        return entry.millis >= start_millis and entry.seq_number > start_seq_number
