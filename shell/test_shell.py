from shell.command import Command
from shell.commands.fullread import FullRead
from shell.commands.fullwrite import FullWrite
from shell.commands.read import Read
from shell.commands.write import Write
from shell.driver import SSDDriver


class TestShell:
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._commands: dict[str, Command] = {}
        self._register_builtin_commands()

    def _register_builtin_commands(self):
        self._commands["write"] = Write(self._driver)
        self._commands["read"] = Read(self._driver)
        self._commands["fullwrite"] = FullWrite(self._driver)
        self._commands["fullread"] = FullRead(self._driver)

    def run(self):
        for _ in range(1):
            line = input("Shell> ").strip()
            if not line:
                return
            parts = line.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in self._commands:
                print(self._commands[cmd].execute(args))