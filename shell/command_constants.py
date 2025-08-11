import re

INVALID_COMMAND = "INVALID COMMAND"
VALID_HEX_PATTERN = re.compile(r"^0x[0-9A-Fa-f]{1,8}$")
VALID_LBA_PATTERN = re.compile(r"[1-9]?[0-9]")
VALID_COMMANDS = {"read", "write", "fullread", "fullwrite", "erase", "erase_range", "exit", "help"}
LBA_START = 0
LBA_END = 100
LBA_RANGE = range(LBA_START, LBA_END)
LBA_MAX = 99
SIZE_RANGE = range(1, 11)
ERASE_SIZE = 10