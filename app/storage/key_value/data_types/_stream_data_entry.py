from dataclasses import dataclass

from typing import Any


@dataclass
class StreamDataEntry:
    millis: int
    seq_number: int
    data: dict[str, Any]
