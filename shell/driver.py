import subprocess
from pathlib import Path


class SSDDriver:
    def read(self, lba: str):
        subprocess.run(
            "python ../device/ssd.py R {}".format(lba),
            shell=True
        )

        output_dir = Path(__file__).resolve().parent.parent / "output"
        ssd_output_file = output_dir / "ssd_output.txt"

        with open(ssd_output_file, "r") as f:
            val = f.readline().rstrip().split()[1]
            return val

    def write(self, lba: str, data: str):
        subprocess.run(
            "python ../device/ssd.py W {} {}".format(lba, data),
            shell=True
        )

        return True
