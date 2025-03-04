from dataclasses import dataclass
from typing import Any

from ._data_entry import DataEntry


@dataclass
class StreamEntry(DataEntry):
    id: str
    data: dict[str, Any]

    def type(self) -> bytes:
        return "+stream\r\n".encode()

    def encode(self) -> bytes:
        return "".encode()
