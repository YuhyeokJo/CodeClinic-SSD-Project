import re

INVALID_COMMAND = "INVALID COMMAND"
VALID_HEX_PATTERN = re.compile(r"^0x[0-9A-Fa-f]{8}$")
VALID_LBA_PATTERN = re.compile(r"[1-9]?[0-9]")
VALID_COMMANDS = {"read", "write", "fullread", "fullwrite", "erase", "erase_range", "exit", "help"}
LBA_START = 0
LBA_END: int = 100
LBA_RANGE = range(LBA_START, LBA_END)
SIZE_RANGE = range(1, 11)
