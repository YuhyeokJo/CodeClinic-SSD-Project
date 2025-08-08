from shell.command import Command
from shell.driver import SSDDriver
from scripts.script_runner import ScriptRunner


class Script1(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        result = self.script_runner.full_write_and_read_compare()
        self.log(f"[{self.name}] {result}", 1)
        return result


class Script2(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        result = self.script_runner.partial_lba_write()
        self.log(f"[{self.name}] {result}", 1)
        return result


class Script3(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        result = self.script_runner.write_read_aging()
        self.log(f"[{self.name}] {result}", 1)
        return result


class Script4(Command):
    def __init__(self, driver: SSDDriver):
        self.script_runner = ScriptRunner(driver)

    def execute(self, args: list[str] = None) -> str:
        result = self.script_runner.erase_and_write_aging()
        self.log(f"[{self.name}] {result}", 1)
        return result
