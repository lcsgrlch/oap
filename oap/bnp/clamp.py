
def clamp(value, minimum, maximum):
    """
    Clamp a number between a minimum and a maximum.

    :param value: value to be clamped
    :param minimum: minimum value
    :param maximum: maximum value
    :return: the clamped value
    """
    return max(minimum, min(value, maximum))


if __name__ == "__main__":
    print(clamp(123, -1.3, 100))
    print(clamp(-12, -1.3, 100))
