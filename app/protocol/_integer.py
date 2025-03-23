from dataclasses import dataclass

from ._resp2_data import Resp2Data


@dataclass
class Integer(Resp2Data):
    data: int

    def resp2_encoded_string(self) -> str:
        return f":{self.data}\r\n"
