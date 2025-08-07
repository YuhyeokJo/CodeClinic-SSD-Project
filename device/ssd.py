from pathlib import Path
from device import Device
import argparse
import re

ERROR = "ERROR"

INITIALIZED_DATA = "0x00000000"
MAX_LBA = 99
MIN_LBA = 0
LBA_RANGE = range(0, MAX_LBA + 1)

MIN_SIZE = -10
MAX_SIZE = 10

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


class Validator:
    def is_valid_lba(self, lba: str) -> bool:
        return lba.isdigit() and MIN_LBA <= int(lba) <= MAX_LBA

    def is_valid_erase_size(self, size: str) -> bool:
        try:
            value = int(size)
            return MIN_SIZE <= value <= MAX_SIZE
        except ValueError:
            return False

    def is_valid_erase_range(self, lba: int, size: int) -> bool:
        if size > 0:
            return lba + size - 1 <= MAX_LBA
        else:
            return lba + size + 1 >= MIN_LBA


class NAND:
    def __init__(self, output_dir):
        self.path = output_dir / "ssd_nand.txt"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        data = {}
        if self.path.exists():
            with open(self.path, "r") as f:
                for line in f:
                    lba, val = line.strip().split()
                    data[lba] = val
        return data

    def save(self, data: dict) -> None:
        with open(self.path, "w") as f:
            for lba, val in data.items():
                f.write(f"{lba} {val}\n")


class OutputWriter:
    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def write(self, content: str):
        with open(self.output_file, "w") as f:
            f.write(content)


class SSD(Device):
    def __init__(self, nand: NAND, validator: Validator, output_writer: OutputWriter):
        self.nand = nand
        self.validator = validator
        self.output_writer = output_writer

    def write(self, lba: str, value: str) -> None:
        if not self.validator.is_valid_lba(lba):
            self._write_error()
            return

        data = self.nand.load()
        data[lba] = value
        self.nand.save(data)

    def read(self, lba: str) -> None:
        if not self.validator.is_valid_lba(lba):
            self._write_error()
            return

        data = self.nand.load()
        result = data.get(lba, INITIALIZED_DATA)
        self._write_output(f"{lba} {result}\n")

    def erase(self, lba: str, size: str) -> None:
        if not self._validate_erase_inputs(lba, size):
            return

        data = self.nand.load()

        for addr in self._erase_range(int(lba), int(size)):
            data[str(addr)] = INITIALIZED_DATA

        self.nand.save(data)

    def _validate_erase_inputs(self, lba: str, size: str) -> bool:
        if not self.validator.is_valid_lba(lba):
            self._write_error()
            return False

        if not self.validator.is_valid_erase_size(size):
            self._write_error()
            return False

        if int(size) == 0:
            return False

        if not self.validator.is_valid_erase_range(int(lba), int(size)):
            self._write_error()
            return False

        return True

    def _write_error(self):
        self.output_writer.write(ERROR)

    def _write_output(self, content: str):
        self.output_writer.write(content)

    def _erase_range(self, lba: int, size: int) -> range:
        if size > 0:
            return range(lba, lba + size)
        else:
            return range(lba + size + 1, lba + 1)


def decimal_lba(lba: str):
    if not lba.isdigit():
        raise argparse.ArgumentTypeError(f"LBA {lba}는 10진수 숫자여야 합니다.")
    return lba


def integer_size(size: str):
    try:
        int(size)
        return size
    except ValueError:
        raise argparse.ArgumentTypeError("Size {size}는 숫자형태여야 합니다.")


def hex_value(value: str):
    if not value.startswith("0x"):
        raise argparse.ArgumentTypeError(f"Value {value}는 '0x'로 시작해야 합니다.")
    if len(value) != 10:
        raise argparse.ArgumentTypeError(f"Value {value}는 총 10자리여야 합니다. 예: 0x1234ABCD")
    hex_part = value[2:]
    if not re.fullmatch(r"[0-9a-fA-F]{8}", hex_part):
        raise argparse.ArgumentTypeError(f"Value {value}는 8자리 16진수여야 합니다 (0-9, A-F).")
    return value[0:2] + hex_part.upper()


def main():
    parser = argparse.ArgumentParser(description="SSD command")
    subparsers = parser.add_subparsers(dest="command")

    write_parser = subparsers.add_parser("W", help="Write")
    write_parser.add_argument("lba", type=decimal_lba)
    write_parser.add_argument("value", type=hex_value, help="Value to write")

    read_parser = subparsers.add_parser("R", help="Read")
    read_parser.add_argument("lba", type=decimal_lba, help="LBA to read from")

    erase_parser = subparsers.add_parser("E", help="Erase")
    erase_parser.add_argument("lba", type=decimal_lba, help="LBA to Erase")
    erase_parser.add_argument("size", type=integer_size, help="Value to write")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        exit(1)

    ssd = SSD(nand=NAND(OUTPUT_DIR), validator=Validator(), output_writer=OutputWriter(OUTPUT_DIR / "ssd_output.txt"))
    if args.command == "W":
        ssd.write(str(args.lba), args.value)
    elif args.command == "R":
        ssd.read(str(args.lba))
    elif args.command == "E":
        ssd.erase(str(args.lba), args.size)


if __name__ == "__main__":
    main()
