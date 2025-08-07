from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def write(self, lba: str, value: str):
        pass

    @abstractmethod
    def read(self, lba: str):
        pass

    @abstractmethod
    def erase(self, lba: str, size: str) -> None:
        pass
