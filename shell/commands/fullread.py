from shell.driver import SSDDriver


class Fullread:
    def __init__(self, driver: SSDDriver):
        self.driver = driver

    def run(self):
        result = {}
        for i in range(100):
            result[i] = self.driver.read(i)
            print(i, result[i])

        return result
