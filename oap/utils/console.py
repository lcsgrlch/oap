"""
Some print functions for console output.
"""

import numpy as np
from oap.__conf__ import MARKER, SLICE_SIZE


def print_array(array, frame=False, scales=True, slice_size=SLICE_SIZE):
    """
    Prints an optical-array as string, list or numpy-array (1d or 2d | dtype=int) to the console output.

    :param array:       optical-array (particle image)
    :type array:        string, list or numpy-array (1d or 2d | dtype=int)

    ::param frame:      show image frame
    :type frame:        boolean

    :param scales:      show pixel scales
    :type scales:       boolean

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer
    """
    if type(array).__module__ == np.__name__:
        if array.ndim >= 2:
            slice_size = len(array[0])
            array = np.ravel(array)
    if frame:
        print("+ ", end='')
        for _ in range(slice_size):
            print("- ", end='')
        print("+ ")
    for y in range(int(len(array)/slice_size)):
        if frame:
            print("| ", end='')
        for x in range(slice_size):
            if array[y*slice_size+x] == 0 or array[y*slice_size+x] == '0':
                print("  ", end='')
            else:
                if scales:
                    print(str(int(array[y*slice_size+x])) + ' ', end='')
                else:
                    if array[y*slice_size+x] == MARKER['poisson']:
                        print("+ ", end='')
                    else:
                        print("\u2588 ", end='')
        if frame:
            print("| ", end='')
        print()
    if frame:
        print("+ ", end='')
        for _ in range(slice_size):
            print("- ", end='')
        print("+ ")


def print_separator(separator='-', slice_size=SLICE_SIZE):
    """
    Prints a simple separator for particle previews to the console output.

    --- optional params ---
    :param separator:   symbol of the separator
    :type separator:    char

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer
    """
    for _ in range(slice_size):
        print(separator + ' ', end='')
    print()
