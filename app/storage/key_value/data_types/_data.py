from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def type(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
