import re
from abc import ABC, abstractmethod

# === Shared Constants ===
VALID_HEX_PATTERN = re.compile(r"^0x[0-9A-Fa-f]{8}$")
VALID_COMMANDS = {"read", "write", "fullread", "fullwrite", "exit", "help", "erase"}
LBA_RANGE = range(0, 100)
MAX_LBA = 100
SIZE_RANGE = range(1, 11)


def is_valid_lba(lba: str) -> bool:
    return lba.isdigit() and int(lba) in LBA_RANGE


def is_valid_hex_data(data: str) -> bool:
    return bool(VALID_HEX_PATTERN.fullmatch(data))


def is_valid_size(size: str) -> bool:
    return size.isdigit() and int(size) in SIZE_RANGE


def is_valid_max_lba(max_lba: str):
    return int(max_lba) <= MAX_LBA


class ArgumentValidator(ABC):
    @abstractmethod
    def validate(self, args: list[str]) -> bool:
        pass


class ReadValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) == 1 and is_valid_lba(args[0])


class WriteValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        if len(args) != 2:
            return False
        lba, data = args
        return is_valid_lba(lba) and is_valid_hex_data(data)


class FullReadValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) == 0


class FullWriteValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) == 1


class HelpValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) > 0 and len(args) <= 1 and (not args or args[0].lower() in VALID_COMMANDS)


class ExitValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) == 0


class EraseValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        if len(args) != 2:
            return False
        lba, size = args
        max_lba = str(int(lba) + int(size) - 1)
        return is_valid_lba(lba) and is_valid_size(size) and is_valid_max_lba(max_lba)


class EraseRangeValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        if len(args) != 2:
            return False
        start_lba, end_lba = args
        size = str(int(end_lba) - int(start_lba) + 1)
        return is_valid_lba(start_lba) and is_valid_size(size) and is_valid_max_lba(end_lba)
