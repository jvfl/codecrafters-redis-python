from dataclasses import dataclass

from typing import Any


@dataclass
class StreamDataEntry:
    millis: int
    seq_number: int
    data: dict[str, Any]

    def formatted_id(self) -> str:
        return f"{self.millis}-{self.seq_number}"

    def to_list(self) -> list[Any]:
        data_as_list = []

        for key, val in self.data.items():
            data_as_list.append(key)
            data_as_list.append(val)

        return [self.formatted_id(), data_as_list]
