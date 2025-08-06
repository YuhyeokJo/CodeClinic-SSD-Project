from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def write(self, address, value):
        pass

    @abstractmethod
    def read(self, address):
        pass
