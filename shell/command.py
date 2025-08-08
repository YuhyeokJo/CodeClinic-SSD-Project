from abc import ABC, abstractmethod
from shell.logger import Logger


class Command(ABC):
    _logger = Logger()

    def log(self, func: str, msg: str):
        self._logger.print(func, msg)

    @abstractmethod
    def execute(self, args: list[str]) -> None:
        pass
