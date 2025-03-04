from dataclasses import dataclass
from typing import Any

from ._data import Data


@dataclass
class StreamData(Data):
    entries: dict[str, dict[str, Any]]

    def type(self) -> bytes:
        return "+stream\r\n".encode()

    def encode(self) -> bytes:
        return "".encode()
