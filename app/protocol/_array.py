from dataclasses import dataclass
from typing import Any

from ._array_codec import ArrayCodec
from ._resp2_data import Resp2Data


@dataclass
class Array(Resp2Data):
    data: list[Any]

    def resp2_encoded_string(self) -> str:
        return ArrayCodec.encode(self.data).decode()
