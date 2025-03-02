from abc import ABC, abstractmethod


class RESPCodecInterface(ABC):
    @abstractmethod
    def encode(self, data: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, data: str) -> str:
        raise NotImplementedError
