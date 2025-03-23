from abc import ABC, abstractmethod


class Resp2Data(ABC):
    @abstractmethod
    def resp2_encoded_string(self) -> str:
        raise NotImplementedError
