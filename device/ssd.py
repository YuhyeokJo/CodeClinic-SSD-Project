from pathlib import Path
from device import Device
import os
import argparse
import re

INITIALIZED_DATA = "0x00000000"


class SSD(Device):
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.ssd_nand_file = self.output_dir / "ssd_nand.txt"
        self.ssd_output_file = self.output_dir / "ssd_output.txt"

    def write(self, lba: str, value: str) -> None:
        if int(lba) < 0 or 99 < int(lba):
            self._write_output("ERROR")
            return

        data = self._load_nand_data()
        data[lba] = value
        self._save_nand_data(data)

    def read(self, lba: str) -> None:
        if int(lba) < 0 or 99 < int(lba):
            self._write_output("ERROR")
            return

        data = self._load_nand_data()
        result = data.get(lba, INITIALIZED_DATA)
        with open(self.ssd_output_file, "w") as f:
            f.write(f"{lba} {result}\n")

    def _write_output(self, content):
        with open(self.ssd_output_file, "w") as f:
            f.write(content)

    def _load_nand_data(self) -> dict:
        data = {}
        if os.path.exists(self.ssd_nand_file):
            with open(self.ssd_nand_file, "r") as f:
                for line in f:
                    lba, val = line.rstrip().split()
                    data[lba] = val
        return data

    def _save_nand_data(self, data: dict) -> None:
        with open(self.ssd_nand_file, "w") as f:
            for lba, val in sorted(data.items()):
                f.write(f"{lba} {val}\n")


def decimal_lba(lba: str):
    if not lba.isdigit():
        raise argparse.ArgumentTypeError(f"LBA {lba}는 10진수 숫자여야 합니다.")
    return int(lba)


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

    try:
        args = parser.parse_args()
    except SystemExit as e:
        exit(1)

    ssd = SSD()
    if args.command == "W":
        ssd.write(args.lba, args.value)
    elif args.command == "R":
        ssd.read(args.lba)


if __name__ == "__main__":
    main()
