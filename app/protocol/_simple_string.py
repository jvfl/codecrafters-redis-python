from dataclasses import dataclass

from ._resp2_data import Resp2Data


@dataclass
class SimpleString(Resp2Data):
    data: str

    @staticmethod
    def OK() -> "SimpleString":
        return SimpleString("OK")

    def resp2_encoded_string(self) -> str:
        return f"+{self.data}\r\n"
