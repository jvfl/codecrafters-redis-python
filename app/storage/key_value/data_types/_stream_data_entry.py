from dataclasses import dataclass

from typing import Any


@dataclass
class StreamDataEntry:
    millis: int
    seq_number: int
    data: dict[str, Any]

    def to_list(self) -> list[Any]:
        data_as_list = []

        for key, val in self.data.items():
            data_as_list.append(key)
            data_as_list.append(val)

        return [
            f"{self.millis}-{self.seq_number}",
            data_as_list,
        ]
