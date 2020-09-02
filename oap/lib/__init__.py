"""
A library of various helpers functions.
"""

import numpy as np
from oap.__conf__ import DEFAULT_TYPE, SLICE_SIZE


# --- Array Type Conversion --------------------------------------------------------------------------------------------

def normalize(array, value=3.0):
    return array.astype(float) / value


def flatten_array(array, slice_size):
    """
    If the optical-array is a two-dimensional numpy-array, it is converted to a 1-dimensional
    array and the slice size is updated. Otherwise the input is equal to the output.

    :param array:       optical-array (particle image)
    :type array:        string, list or numpy-array (1d or 2d | dtype=int)

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            tuple - (optical-array : string, list or numpy-array (1d or 2d | dtype=int),
                                 slice size : integer)
    """
    if type(array).__module__ == np.__name__:
        if array.ndim == 2:
            slice_size = array.shape[1]
            array = np.ravel(array)
    return array, slice_size


def check_array_type(array, slice_size=SLICE_SIZE):
    """
    Returns a string that describes the type of the data structure. If the optical-array
    is a 2-dimensional numpy-array, it is also converted to a 1-dimensional array
    and the slice size will be updated.

    :param array:       optical-array (particle image)
    :type array:        string, list or numpy-array (1d or 2d | dtype=int)

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            3-tuple - (optical-array : string, list or numpy-array (1d or 2d | dtype=int),
                                   data type : string,
                                   slice size : integer)
    """
    data_type = DEFAULT_TYPE
    if type(array) is str:
        data_type = "STRING"
    elif type(array) is list:
        data_type = "LIST"
    elif type(array).__module__ == np.__name__:
        if array.ndim == 2:
            data_type = "ARRAY2D"
            slice_size = array.shape[1]
            array = np.ravel(array)
        else:
            data_type = "ARRAY"
    return array, data_type, slice_size


def convert_array_to_type(array, as_type, slice_size=SLICE_SIZE):
    """
    Converts a one-dimensional numpy-array to a given data type.

    :param array:       optical-array (particle image)
    :type array:        string, list or numpy-array (1d or 2d | dtype=int)

    :param as_type:     data type of the returned optical-array ("array", "array2d", "list", "string")
    :type as_type:      string

    --- optional params ---
    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            optical-array as string, list or numpy-array (1d or 2d | dtype=int)
    """
    if as_type.upper() == "STRING" or as_type.upper() == "STR":
        array = ''.join([str(a) for a in array])
    elif as_type.upper() == "LIST":
        array = array.tolist()
    elif as_type.upper() == "ARRAY2D":
        array = array.reshape(-1, slice_size)
    return array
