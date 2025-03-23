from dataclasses import dataclass

from ._data import Data
from ._stream_data_entry import StreamDataEntry


@dataclass
class StreamData(Data):
    entries: list[StreamDataEntry]

    def type(self) -> str:
        return "stream"

    def encode(self) -> bytes:
        return "".encode()
