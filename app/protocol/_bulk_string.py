from dataclasses import dataclass
from typing import Optional

from ._resp2_data import Resp2Data
from ._bulk_string_codec import BulkStringCodec


@dataclass
class BulkString(Resp2Data):
    data: Optional[str]

    def resp2_encoded_string(self) -> str:
        return BulkStringCodec.encode(self.data).decode()
