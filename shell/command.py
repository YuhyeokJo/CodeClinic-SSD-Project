from abc import ABC, abstractmethod
from shell.logger import Logger


class Command(ABC):
    _logger = Logger()

    def log(self, command_name: str, msg: str):
        func = f"{command_name}.execute()"
        self._logger.print(func, msg)

    @abstractmethod
    def execute(self, args: list[str]) -> None:
        pass
