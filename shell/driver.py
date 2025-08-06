import subprocess


class SSDDriver:
    def read(self, lba: str):
        subprocess.run(
            "ssd R {}".format(lba),
            cwd=r"../device",
            shell=True
        )

    def write(self, lba: str, data: str):
        subprocess.run(
            "ssd W {} {}".format(lba, data),
            cwd=r"../device",
            shell=True
        )
