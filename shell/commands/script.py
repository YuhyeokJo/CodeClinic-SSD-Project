from shell.driver import SSDDriver
from shell.command import Command
from shell.commands.write import Write
from shell.commands.read import Read

INVALID = "INVALID"
SCRIPT_INVALID_COMMAND = "[SCRIPT] INVALID COMMAND"
SCRIPT_PASS = "[SCRIPT] PASS"
SCRIPT_FAIL = "[SCRIPT] FAIL"

class Script(Command):
    def __init__(self, driver):
        self.write_command = Write(driver)
        self.read_command = Read(driver)

    def execute(self, args: list[str]) -> str:
        res = self.write_command.execute(args)
        if INVALID in res:
            return SCRIPT_INVALID_COMMAND
        return self._read_comapre(args)

    def _read_comapre(self, args: list[str]) -> str:
        lba, data = args[0], args[1]
        res = self.read_command.execute([lba])
        if res.split(" ")[-1] != data:
            return SCRIPT_FAIL
        return SCRIPT_PASS

