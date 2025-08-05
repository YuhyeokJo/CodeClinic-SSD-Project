from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def write(self, cmd, address, value):
        pass

    @abstractmethod
    def read(self, cmd, address):
        pass
