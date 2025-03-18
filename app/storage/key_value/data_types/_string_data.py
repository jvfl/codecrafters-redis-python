from dataclasses import dataclass

from app.protocol import BulkStringCodec

from ._data import Data


@dataclass
class StringData(Data):
    data: str

    def type(self) -> bytes:
        return "+string\r\n".encode()

    def encode(self) -> bytes:
        return BulkStringCodec.encode(self.data)
