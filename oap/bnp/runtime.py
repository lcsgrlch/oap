import time


class Runtime:

    def __init__(self, decimals=3):
        self.start_time = 0
        self.decimals = decimals

    def start(self):
        self.start_time = time.perf_counter()
        return self

    def stop(self,):
        print(f"Runtime {round(time.perf_counter() - self.start_time, self.decimals)}s")
