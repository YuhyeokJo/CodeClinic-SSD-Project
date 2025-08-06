from shell.command import Command
from shell.driver import SSDDriver


class Help(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._help_map = {
            "READ": "read <LBA> <Value>: Reads value from given LBA",
            "WRITE": "write <LBA>: Writes value to LBA",
            "FULLREAD": "fullread: Reads value from all LBA(0~99)",
            "FULLWRITE": "fullwrite <Value>:  Writes value to all LBA(0~99)",
            "EXIT": "exit: Exit shell"
        }

    def execute(self, args: list[str]) -> str:
        if not args:
            available = "\n".join(f"- {cmd}" for cmd in self._help_map)
            return f"Available commands:\n{available}"

        cmd = args[0]
        cmd_upper = cmd.upper()
        if cmd_upper in self._help_map:
            return self._help_map[cmd_upper]
        return f"Unknown command: {cmd}"
