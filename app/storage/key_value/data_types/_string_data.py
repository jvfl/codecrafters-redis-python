from dataclasses import dataclass

from app.protocol import BulkStringCodec

from ._data import Data

STRING_CODEC = BulkStringCodec()


@dataclass
class StringData(Data):
    data: str

    def type(self) -> bytes:
        return "+string\r\n".encode()

    def encode(self) -> bytes:
        return STRING_CODEC.encode(self.data).encode()
