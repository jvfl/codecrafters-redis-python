from typing import Any

from app.protocol import ArrayCodec
from app.storage.key_value.data_types import StreamData, StreamDataEntry
from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("XRANGE")
class XRangeCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]
        start = args[1]
        end = args[2]

        data = await self._keys_storage.retrieve(key)

        if data is None or not isinstance(data, StreamData):
            await writer.write(ArrayCodec.encode([]))
            return

        entries = [entry for entry in data.entries if self.in_range(entry, start, end)]
        response = [
            [
                f"{entry.millis}-{entry.seq_number}",
                self.to_list(entry.data),
            ]
            for entry in entries
        ]

        print(response)

        await writer.write(ArrayCodec.encode(response))

    def to_list(self, data: dict[str, Any]) -> list[Any]:
        output = []

        for key, val in data.items():
            output.append(key)
            output.append(val)

        return output

    def in_range(self, entry: StreamDataEntry, start: str, end: str) -> bool:
        start_millis, start_seq_number = [0, 0]
        if start != "-":
            start_millis, start_seq_number = [int(raw) for raw in start.split("-")]

        end_millis, end_seq_number = [int(raw) for raw in end.split("-")]

        return (
            entry.millis >= start_millis
            and entry.seq_number >= start_seq_number
            and entry.millis <= end_millis
            and entry.seq_number <= end_seq_number
        )
