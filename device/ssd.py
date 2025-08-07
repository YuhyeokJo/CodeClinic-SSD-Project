from pathlib import Path
from device import Device
import os
import argparse
import re

INITIALIZED_DATA = "0x00000000"


class Validator:
    def is_valid_lba(self, lba: str) -> bool:
        return lba.isdigit() and 0 <= int(lba) <= 99

    def is_valid_erase_size(self, size: str) -> bool:
        try:
            value = int(size)
            return -10 <= value <= 10
        except ValueError:
            return False


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


class SSD(Device):
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.ssd_output_file = self.output_dir / "ssd_output.txt"
        self.nand = NAND(self.output_dir)
        self.validator = Validator()

    def write(self, lba: str, value: str) -> None:
        if not self.validator.is_valid_lba(lba):
            self._write_output("ERROR")
            return

        data = self.nand.load()
        data[lba] = value
        self.nand.save(data)

    def read(self, lba: str) -> None:
        if not self.validator.is_valid_lba(lba):
            self._write_output("ERROR")
            return

        data = self.nand.load()
        result = data.get(lba, INITIALIZED_DATA)
        with open(self.ssd_output_file, "w") as f:
            f.write(f"{lba} {result}\n")

    def erase(self, lba: str, size: str) -> None:
        if not self.validator.is_valid_lba(lba):
            self._write_output("ERROR")
            return

        if not self.validator.is_valid_erase_size(size):
            self._write_output("ERROR")
            return

        if int(size) == 0:
            return

        lba_int = int(lba)
        size_int = int(size)
        if size_int > 0:
            max_addr = lba_int + size_int - 1
            if max_addr > 99:
                size_int = 99 - lba_int + 1
        elif size_int < 0:
            min_addr = lba_int + size_int
            if min_addr < 0:
                size_int = -lba_int

        size = str(size_int)
        data = self.nand.load()
        # forward erase
        if int(size) > 0:
            for addr in range(int(lba), int(lba) + int(size), 1):
                data[str(addr)] = INITIALIZED_DATA
        else:
            for addr in range(int(lba) + int(size), int(lba) + 1, 1):
                data[str(addr)] = INITIALIZED_DATA

        self.nand.save(data)

    def _write_output(self, content):
        with open(self.ssd_output_file, "w") as f:
            f.write(content)


def decimal_lba(lba: str):
    if not lba.isdigit():
        raise argparse.ArgumentTypeError(f"LBA {lba}는 10진수 숫자여야 합니다.")
    return lba


def decimal_size(size: str):
    if not size.isdigit():
        raise argparse.ArgumentTypeError(f"Size {size}는 10진수 숫자여야 합니다.")
    return size


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
    erase_parser.add_argument("size", type=decimal_lba, help="Value to write")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        exit(1)

    ssd = SSD()
    if args.command == "W":
        ssd.write(str(args.lba), args.value)
    elif args.command == "R":
        ssd.read(str(args.lba))
    elif args.command == "E":
        ssd.erase(str(args.lba), args.size)


if __name__ == "__main__":
    main()
