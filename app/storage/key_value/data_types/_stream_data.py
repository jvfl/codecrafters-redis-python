from dataclasses import dataclass

from ._data import Data
from ._stream_data_entry import StreamDataEntry


@dataclass
class StreamData(Data):
    entries: list[StreamDataEntry]

    def type(self) -> bytes:
        return "+stream\r\n".encode()

    def encode(self) -> bytes:
        return "".encode()
