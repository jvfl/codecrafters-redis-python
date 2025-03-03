import struct
from typing import Tuple, Union
from pathlib import Path

from ._auxiliary_field import AuxiliaryField
from ._rdb_data import RDBData


class RDBReader:
    AUX_HEADER = b"\xfa"
    SELECTDB_HEADER = b"\xfe"
    RESIZEDB_HEADER = b"\xfb"
    END_HEADER = b"\xff"

    SIGNED_INT_8 = 0
    SIGNED_INT_16 = 1
    SIGNED_INT_32 = 2

    def __init__(self, file_path: Path):
        self.file = open(file_path, "rb")

    def read(self):
        magic_string = self.file.read(5)
        _ = self.file.read(4)  # version

        if magic_string != b"REDIS":
            raise ValueError("Invalid RDB file")

        next_section = self.file.read(1)

        auxiliary_fields = []
        while next_section == self.AUX_HEADER:
            auxiliary_fields.append(self.read_auxiliary_field())
            next_section = self.file.read(1)

        if next_section == self.SELECTDB_HEADER:
            _, length = self.read_encoded_length()
            next_section = self.file.read(1)

        if next_section == self.RESIZEDB_HEADER:
            _, hash_table_size = self.read_encoded_length()
            _, expires_size = self.read_encoded_length()
            next_section = self.file.read(1)

        hash_table = {}
        if next_section == b"\x00":
            key = self.read_string()
            value = self.read_string()
            hash_table[key] = value

            next_section = self.file.read(1)

        if next_section == self.END_HEADER:
            return RDBData(auxiliary_fields, hash_table)

    def read_auxiliary_field(self):
        key = self.read_string()
        value = self.read_string()
        return AuxiliaryField(key, value)

    def read_encoded_length(self) -> Tuple[bool, int]:
        length_encoding = struct.unpack("B", self.file.read(1))[0]

        two_most_significant_bytes = (length_encoding & 0b11000000) >> 6

        if two_most_significant_bytes == 0b00:
            length = length_encoding & 0b00111111
            return (False, length)
        elif two_most_significant_bytes == 0b01:
            print("1")
            pass
        elif two_most_significant_bytes == 0b10:
            print("2")
            pass
        elif two_most_significant_bytes == 0b11:
            return (True, length_encoding & 0b00111111)

        raise ValueError("Unsupported encoded length", two_most_significant_bytes)

    def read_string(self) -> Union[int, str]:
        is_encoded, length = self.read_encoded_length()

        if is_encoded:
            return self.read_encoded_int(length)

        return self.file.read(length).decode()

    def read_encoded_int(self, int_type_code: int) -> int:
        if int_type_code == self.SIGNED_INT_8:
            return struct.unpack("b", self.file.read(1))[0]
        if int_type_code == self.SIGNED_INT_16:
            return struct.unpack("h", self.file.read(2))[0]
        if int_type_code == self.SIGNED_INT_32:
            return struct.unpack("i", self.file.read(4))[0]
        else:
            raise ValueError("Unsupported encoded int", int_type_code)
