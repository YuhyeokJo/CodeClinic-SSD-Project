from shell.command import Command
from shell.command_validator import HelpValidator
from shell.driver import SSDDriver


class Help(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = HelpValidator()
        self._help_map = {
            "read": "read <LBA> <Value> (Reads value from given LBA)",
            "write": "write <LBA> (Writes value to LBA)",
            "fullread": "fullread: (Reads value from all LBA(0~99))",
            "fullwrite": "fullwrite <Value> (Writes value to all LBA(0~99))",
            "help": "help (Print Usage)",
            "exit": "exit (Exit shell)"
        }

    def format_help(self, cmd: str, usage: str) -> str:
        return f"""
                SSD Test Shell Tool
                Team: ✨Code Clinic✨
                Author: 조유혁(팀장님), 강동협, 김혜원, 배정은, 조보근
                Command: {cmd.lower()}
                Usage & Description: {usage}
                """

    def execute(self, args: list[str]) -> str:
        if not self._validator.validate(args):
            return "INVALID COMMAND"

        cmd = args[0].lower()
        return self.format_help(cmd, self._help_map[cmd])
