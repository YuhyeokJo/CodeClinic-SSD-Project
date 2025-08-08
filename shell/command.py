from abc import ABC, abstractmethod
from logger import Logger


class Command(ABC):
    _logger = Logger()

    def __init__(self, name: str):
        self._name = name

    def log(self, func: str, msg: str):
        self._logger.print(func, msg)

    @abstractmethod
    def execute(self, args: list[str]) -> None:
        pass
