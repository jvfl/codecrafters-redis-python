import math

from app.protocol import Resp2Data, Array
from app.storage.key_value.data_types import StreamData, StreamDataEntry
from app.io import ConnectionManager

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("XRANGE")
class XRangeCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        key = args[0]
        start = args[1]
        end = args[2]

        data = await self._keys_storage.retrieve(key)

        if data is None or not isinstance(data, StreamData):
            return Array([])

        entries = [entry for entry in data.entries if self.in_range(entry, start, end)]
        response = [entry.to_list() for entry in entries]

        return Array(response)

    def in_range(self, entry: StreamDataEntry, start: str, end: str) -> bool:
        start_millis, start_seq_number = [0, 0]
        if start != "-":
            start_millis, start_seq_number = [int(raw) for raw in start.split("-")]

        end_millis, end_seq_number = [math.inf, math.inf]
        if end != "+":
            end_millis, end_seq_number = [int(raw) for raw in end.split("-")]

        return (
            entry.millis >= start_millis
            and entry.seq_number >= start_seq_number
            and entry.millis <= end_millis
            and entry.seq_number <= end_seq_number
        )
