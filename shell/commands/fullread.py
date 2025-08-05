from shell.driver import SSDDriver


class Fullread:
    def __init__(self, driver: SSDDriver):
        self.driver = driver

    def run(self):
        result = {}
        for lba in range(100):
            result[lba] = self.driver.read(str(lba))

        return result
