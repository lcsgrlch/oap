import time
import threading


class Loading:

    def __init__(self, prefix="", suffix="", mode="spin", speed=0.3, animation="|/-\\",
                 symbol=".", length=4, runtime=False):
        """
        Simple loading animation for console output. Runs as a separate thread.

        :param prefix: text before the loading animation (string)
        :param suffix: text after the loading animation (string)
        :param mode: type of loading animation (string) - possible values: bar, spin
        :param speed: iteration time in seconds (float)
        :param animation: spin animation chars (string)
        :param symbol: loading symbol if mode is "bar" (string)
        :param length: length of the loading bar (integer)
        :param runtime: show runtime after stop (boolean)
        """
        self.loading = False
        self.prefix = prefix
        self.suffix = suffix
        self.speed = speed
        self.animation = animation
        self.symbol = symbol
        self.length = length
        self.runtime = runtime
        self.__start_time = None
        self.mode = mode.lower()
        self.__validation()

    def __validation(self):
        if self.mode not in ["bar", "spin"]:
            raise ValueError("Value of mode is invalid. Valid values for mode: bar, spin")

    def __bar(self, prefix, suffix):
        idx = 0
        while self.loading:
            print(f"\r{prefix}" + (idx % self.length) * self.symbol
                  + ((self.length-1) - idx % self.length) * " " + f"{suffix}", end="")
            idx += 1
            if idx >= self.length * 1000:
                idx = 0
            time.sleep(self.speed)

    def __spin(self, prefix, suffix):
        idx = 0
        while self.loading:
            print(f"\r{prefix}{self.animation[idx % len(self.animation) - 1]}{suffix}", end="")
            idx += 1
            if idx >= len(self.animation) * 1000:
                idx = 0
            time.sleep(self.speed)

    def start(self, prefix=None, suffix=None):
        self.loading = True
        self.__start_time = time.perf_counter()
        prefix = self.prefix if prefix is None else prefix
        suffix = self.suffix if suffix is None else suffix
        self.__validation()
        method = self.__spin if self.mode == "spin" else self.__bar
        threading.Thread(target=method, args=(prefix, suffix)).start()
        return self

    def stop(self, msg=None):
        if self.loading:
            self.loading = False
            seconds = round(time.perf_counter() - self.__start_time, 3)
            print("\r", end="")
            if msg is not None and not self.runtime:
                print(msg)
            elif msg is not None and self.runtime:
                print(f"{msg}Runtime {seconds}s")
            elif msg is None and self.runtime:
                print(f"Runtime {seconds}s")


if __name__ == "__main__":
    loading = Loading(prefix="Spinning ", runtime=True).start()
    time.sleep(3)
    loading.stop(msg="Spinning completed! ")

    loading = Loading(prefix="And vice versa! ", runtime=True, animation="|\\-/").start()
    time.sleep(3)
    loading.stop()

    loading = Loading(prefix="Loading", mode="bar").start()
    time.sleep(3)
    loading.stop(msg="Loading completed!")

    loading = Loading(prefix="Calculating [", suffix="]", mode="bar", symbol="=", length=10).start()
    time.sleep(6)
    loading.stop(msg="Calculation completed!")

    loading.start("Processing [")
    time.sleep(3)
    loading.stop(msg="Processing completed!")
