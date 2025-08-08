from shell.command import Command
from shell.command_constants import INVALID_COMMAND
from shell.command_validator import WriteValidator
from shell.driver import SSDDriver


class Write(Command):
    def __init__(self, driver: SSDDriver):
        self._driver = driver
        self._validator = WriteValidator()

    def normalize_hex_data(self, data: str) -> str:
        hex_prefix = data[:2]
        hex_digits = data[2:]
        return f"{hex_prefix}{hex_digits.zfill(8)}"

    def execute(self, args: list[str]) -> str:
        args = [args[0], self.normalize_hex_data(args[1])]
        if not self._validator.validate(args):
            result =  INVALID_COMMAND
        else:
            lba, data = args
            result = self._driver.write(lba, data)

            if not result:
                result = f"[{self.name}] Fail"
            else:
                result = f"[{self.name}] Done"
        self.log(result)
        return result
