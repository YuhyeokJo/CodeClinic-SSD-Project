from abc import ABC, abstractmethod

from shell.logger import Logger


class Command(ABC):
    _logger = Logger()

    @property
    def name(self):
        return self.__class__.__name__

    def log(self, msg: str, level: int):
        func = f"{self.name}.execute()"
        func = level * ' ' + func
        self._logger.print(func, msg)

    @abstractmethod
    def execute(self, args: list[str]) -> None:
        pass
