try:
    from __oap_c.core import (
        decompress as __decompress,
        OpticalArray
    )
except ModuleNotFoundError:
    error_msg = "C extension of oap library is not compiled yet!"
    print("Catching ModuleNotFoundError:", error_msg)


def decompress(*args, **kwargs):
    return __decompress(*args, **kwargs)
