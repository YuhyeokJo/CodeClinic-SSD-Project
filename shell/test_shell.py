from shell.command import Command
from shell.commands.fullread import Fullread
from shell.commands.fullwrite import FullWrite
from shell.commands.read import ReadCommand
from shell.commands.write import WriteCommand
from shell.driver import SSDDriver


class TestShell:
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._commands: dict[str, Command] = {}
        self._register_builtin_commands()

    def _register_builtin_commands(self):
        self._commands["write"] = WriteCommand(self._driver)
        self._commands["read"] = ReadCommand(self._driver)
        self._commands["fullwrite"] = FullWrite(self._driver)
        self._commands["fullread"] = Fullread(self._driver)


