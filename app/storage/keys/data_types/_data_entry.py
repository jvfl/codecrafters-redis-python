from abc import ABC, abstractmethod


class DataEntry(ABC):
    @abstractmethod
    def type(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
