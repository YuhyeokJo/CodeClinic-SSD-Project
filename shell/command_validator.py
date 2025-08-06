import re
from abc import ABC, abstractmethod

# === Shared Constants ===
VALID_HEX_PATTERN = re.compile(r"^0x[0-9A-Fa-f]{8}$")
VALID_COMMANDS = {"read", "write", "fullread", "fullwrite", "exit", "help"}
LBA_RANGE = range(0, 100)

def is_valid_lba(lba: str) -> bool:
    return lba.isdigit() and int(lba) in LBA_RANGE

def is_valid_hex_data(data: str) -> bool:
    return bool(VALID_HEX_PATTERN.fullmatch(data))

class ArgumentValidator(ABC):
    @abstractmethod
    def validate(self, args: list[str]) -> bool:
        pass

class ReadValidator(ArgumentValidator):
    def validate(self, args: list[str]) -> bool:
        return len(args) == 1 and is_valid_lba(args[0])

