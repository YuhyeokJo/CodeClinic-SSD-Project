from shell.driver import SSDDriver
from shell.command import Command
from shell.commands.write import Write
from shell.commands.read import Read


class Script(Command):
    def __init__(self, driver):
        self.write_command = Write(driver)
        self.read_command = Read(driver)


    def execute(self, args: list[str]) -> str:
        res = self.write_command.execute(args)
        if "INVALID" in res:
            return "[SCRIPT] INVALID COMMAND"
        self._read_comapre(args)

    def _read_comapre(self, args):
        pass

