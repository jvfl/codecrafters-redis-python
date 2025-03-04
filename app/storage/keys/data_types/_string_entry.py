from dataclasses import dataclass

from app.protocol import BulkStringCodec

from ._data_entry import DataEntry

STRING_CODEC = BulkStringCodec()


@dataclass
class StringEntry(DataEntry):
    data: str

    def type(self) -> bytes:
        return "+string\r\n".encode()

    def encode(self) -> bytes:
        return STRING_CODEC.encode(self.data).encode()
