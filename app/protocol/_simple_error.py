from dataclasses import dataclass

from ._resp2_data import Resp2Data


@dataclass
class SimpleError(Resp2Data):
    data: str

    def resp2_encoded_string(self) -> str:
        return f"-ERR {self.data}\r\n"
