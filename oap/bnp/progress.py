
def progress(iteration, total, prefix="", suffix="", decimals=1, length=20):
    """
    Show the progress. Perfect for loops.

    :param iteration: loop (integer)
    :param total: number of iterations (integer)
    :param prefix: text before the progressbar (string)
    :param suffix: text after the progressbar (string)
    :param decimals: decimals of the percentage display (integer)
    :param length: length of the progress bar (integer)
    """
    if (total-1) <= 0:
        return
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / (total-1)))
    filled = int(length * iteration // (total-1))
    bar = "=" * filled + '.' * (length - filled)
    print(f"\r{prefix}[{bar}] {percent}%{suffix}", end="")
    if iteration == (total-1):
        print()


if __name__ == "__main__":

    import time
    limit = 1000
    for i in range(limit):
        progress(i, limit, "Loading... ", " Complete")
        time.sleep(0.01)
