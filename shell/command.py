from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, args: list[str]) -> None:
        pass