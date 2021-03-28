"""
Various functions for the analysis and modification of optical-arrays.
"""

import numpy as np
from oap.lib import check_array_type, convert_array_to_type, flatten_array
from oap.__conf__ import MARKER, MONOSCALE_SHADOWLEVEL, SLICE_SIZE


# --- Features ---------------------------------------------------------------------------------------------------------

def barycenter(array, coordinates=True, slice_size=SLICE_SIZE):
    """
    Calculates the barycenter of an OAP image. Returns the particle barycenter
    as integer coordinates for the array or as exact floating point values.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 dimensional) or list or string

    --- optional params ---
    :param coordinates: rounds barycenter to integer values (default == True)
    :type coordinates:  boolean

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            x- and y-value of barycenter
    """
    array, slice_size = flatten_array(array, slice_size)

    sum_x = 0
    sum_y = 0
    number_of_pixels = 0

    for y in range(int(len(array) / slice_size)):
        for x in range(slice_size):
            if array[y*slice_size+x] != 0 and array[y*slice_size+x] != '0':
                sum_x += x
                sum_y += y
                number_of_pixels += 1

    if not number_of_pixels:
        raise ValueError("no shaded pixels in the particle image")

    if coordinates:
        x_bary = int(round(sum_x / float(number_of_pixels)))
        y_bary = int(round(sum_y / float(number_of_pixels)))
        return y_bary, x_bary
    else:
        x_bary = sum_x / float(number_of_pixels)
        y_bary = sum_y / float(number_of_pixels)
        return y_bary, x_bary


def features(array, slice_size=SLICE_SIZE):
    """
    Analyses an optical-array as numpy-array, list or string and
    returns its properties.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            dict of particle features
    """
    array, slice_size = flatten_array(array, slice_size)

    array = clip_y(array, slice_size=slice_size)
    y_dim = int(len(array) / slice_size)

    min_index = slice_size - 1
    max_index = 0
    min_poisson_index = slice_size - 1
    max_poisson_index = 0

    for y in range(y_dim):
        for x in range(slice_size):
            if array[y*slice_size+x] != 0 and array[y*slice_size+x] != '0':
                if x > max_index:
                    max_index = x
                if x < min_index:
                    min_index = x
            if array[y*slice_size+x] == MARKER['poisson'] or array[y*slice_size+x] == str(MARKER['poisson']):
                if x > max_poisson_index:
                    max_poisson_index = x
                if x < min_poisson_index:
                    min_poisson_index = x

    poisson_diameter = max_poisson_index-min_poisson_index+1

    result_set = {'height': y_dim, 'width': max_index-min_index+1,
                  'poisson': poisson_diameter if poisson_diameter > 0 else 0,
                  'min_index': min_index, 'max_index': max_index}
    return result_set


# --- Array Modifications ----------------------------------------------------------------------------------------------

def adjust_y(array, new_y, warning=False, as_type=None, slice_size=SLICE_SIZE):
    """
    Converts the optical-array length to a specific length corresponding to
    the wished image height.

    Image input is possible as 1 dimensional list, string or numpy-array.
    Returns a new numpy-array with a fixed size, corresponding to the
    image height and the given slice size.

    Caution, this function clips particle images, which are to large.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    :param new_y:        new y-dimension
    :type new_y:         integer

    --- optional params ---
    :param warning:     prints a warning when clipping (default == False)
    :type warning:      boolean

    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new optical-array without empty slices
    """
    array, data_type, slice_size = check_array_type(array, slice_size)

    if warning:
        if new_y * slice_size < len(array):
            print("\nWarning (oap::adjust_y) new y-dimension too small: particle gets clipped\n")

    new_array = np.zeros(new_y*slice_size, dtype=int)

    for y in range(int(min(new_y, len(array)/slice_size))):
        for x in range(slice_size):
            if array[y*slice_size+x] != 0 and array[y*slice_size+x] != '0':
                new_array[y*slice_size+x] = array[y*slice_size+x]
    return convert_array_to_type(new_array, as_type=as_type if as_type else data_type, slice_size=slice_size)


def clip_y(array, as_type=None, slice_size=SLICE_SIZE):
    """
    Deletes all empty image slices in the optical-array.

    Note: If there are empty image slices between the shaded pixels, they will be deleted as well.
    This can happen in rare cases when converting from grayscale to monoscale.
    This would lead to a compression of the imaged cloud particle.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:   width of the optical-array (number of diodes)
    :type slice_size:    integer

    :return:            new optical-array without empty slices
    """
    array, data_type, slice_size = check_array_type(array, slice_size)

    new_array = []

    for y in range(int(len(array)/slice_size)):
        if max(array[y*slice_size:y*slice_size+slice_size]):
            new_array.append(array[y*slice_size:y*slice_size+slice_size])
    return convert_array_to_type(np.ravel(new_array), as_type=as_type if as_type else data_type, slice_size=slice_size)


def _flip_array(array, axis, slice_size=SLICE_SIZE):
    """
    Flips an optical-array in x- or y-direction.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    :param axis:       axis or axes along which to flip over
    :type axis:        integer (values: 0 or 1)

    --- optional params ---
    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            flipped optical-array
    """
    if type(array).__module__ == np.__name__:
        if array.ndim == 2:
            return np.flip(array, axis=axis)
        else:
            array = array.reshape(-1, slice_size)
            array = np.flip(array, axis=axis)
            return np.ravel(array)
    elif type(array) is str:
        array = np.array(list(array), dtype=int).reshape(-1, slice_size)
        array = np.flip(array, axis=axis)
        return ''.join([str(a) for a in np.ravel(array)])
    elif type(array) is list:
        new_array = np.array(array, dtype=int).reshape(-1, slice_size)
        new_array = np.flip(new_array, axis=axis)
        if type(array[0]) is str:
            return [str(a) for a in np.ravel(new_array)]
        return np.ravel(new_array).tolist()


def flip_x(array, slice_size=SLICE_SIZE):
    """
    Flips an optical-array in x-direction.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            flipped optical-array
    """
    return _flip_array(array, 1, slice_size=slice_size)


def flip_y(array, slice_size=SLICE_SIZE):
    """
    Flips an optical-array in y-direction.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            flipped optical-array
    """
    return _flip_array(array, 0, slice_size=slice_size)


# ToDo: not implemented
def monochromatic(array, color=MONOSCALE_SHADOWLEVEL, as_type=None, slice_size=SLICE_SIZE):
    """
    Converts a greyscale optical-array with different colors for their shadow levels,
    by setting all shadow levels to one color value. This is usually the Monoscale
    Shadow Level, which is equal to 2 (50 percent dimming of the laser intensity).

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param color:       value of color
    :type color:        char or integer

    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new optical-array - every pixel has the same color
    """
    # array, data_type, slice_size = check_array_type(array, slice_size)

    array[array >= 1] = color

    # new_array = np.zeros(len(array), dtype=int)
    # for y in range(int(len(array)/slice_size)):
    #     for x in range(slice_size):
    #         if array[y*slice_size+x] != 0 and array[y * slice_size + x] != '0':
    #             if array[y*slice_size+x] in [1, 2, 3]:
    #                 new_array[y*slice_size+x] = color
    #             elif array[y*slice_size+x] in ['1', '2', '3']:
    #                 new_array[y*slice_size+x] = str(color)
    #             else:
    #                 new_array[y*slice_size+x] = array[y*slice_size+x]
    # return convert_array_to_type(array, as_type=as_type if as_type else data_type, slice_size=slice_size)


def monoscale(array, color=MONOSCALE_SHADOWLEVEL, as_type=None, slice_size=SLICE_SIZE):
    """
    Converts a grayscale array into a monoscale array.
    This deletes shadow level 1 and sets the other shadow values to a uniform value.
    The Poisson spot markings remain unchanged.

    Note: After conversion, the optical-array may not contain any shaded pixels.
          Also, empty image slices can occur in the image.

    If the optical-array does not contain shaded pixels, the function returns None.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param color:       value of monoscale color
    :type color:        char or integer

    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new monoscale optical-array
    """
    array, data_type, slice_size = check_array_type(array, slice_size)

    new_array = np.zeros(len(array), dtype=int)
    for y in range(int(len(array)/slice_size)):
        for x in range(slice_size):
            if array[y*slice_size+x] not in [0, 1, '0', '1']:
                if array[y*slice_size+x] in [2, 3]:
                    new_array[y*slice_size+x] = color
                elif array[y * slice_size + x] in ['2', '3']:
                    new_array[y * slice_size + x] = str(color)
                else:
                    new_array[y*slice_size+x] = array[y*slice_size+x]
    return convert_array_to_type(new_array, as_type=as_type if as_type else data_type,
                                 slice_size=slice_size) if max(new_array) else None


def move_to_x(array, new_x, clip=True, as_type=None, slice_size=SLICE_SIZE):
    """
    Calculates the barycenter of a particle and shifts the particle (in the image)
    to the given position in x-direction.

    Returns the new shifted particle image. The x-coordinate of the barycenter is
    equal to the new position.

    If clip is false, pixels which get pushed out of the picture frame, will
    appear on the other side of the picture.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    :param new_x:       new x-value for the barycenter
    :type new_x:        integer

    --- optional params ---
    :param clip:        pixels that are moved out of the picture frame are lost (default == True)
    :type clip:         boolean

    :param as_type:     data type of the returned optical-array ("array", "array2d", "list", "string")
    :type as_type:      string

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new optical-array with shifted particle
    """
    array, data_type, slice_size = check_array_type(array, slice_size)

    # Calculate the shift.
    _, x_bary = barycenter(array, coordinates=True, slice_size=slice_size)
    x_shift = new_x - x_bary

    new_array = np.zeros(len(array), dtype=int)

    for y in range(int(len(array)/slice_size)):
        for x in range(slice_size):
            if not array[y*slice_size+x] == 0 and not array[y*slice_size+x] == '0':
                if clip:
                    # Pixels which get pushed out of the picture frame, will
                    # be clipped. !!! Loss Of Information !!!
                    if (y*slice_size+slice_size-1) >= (y*slice_size+x+x_shift) >= 0 \
                            and slice_size > (x+x_shift) >= 0:
                        new_array[y*slice_size+x+x_shift] = array[y*slice_size+x]
                else:
                    # Pixels which get pushed out of the picture frame, will
                    # appear on the other side of the picture.
                    new_x = (x+x_shift) % slice_size
                    new_array[y*slice_size+new_x] = array[y*slice_size+x]
    return convert_array_to_type(new_array, as_type=as_type if as_type else data_type, slice_size=slice_size)


def move_to_y(array, new_y, clip=True, as_type=None, slice_size=SLICE_SIZE):
    """
    Calculates the barycenter of a particle and shifts the particle (in the image)
    to the given position in y-direction.

    This only works for a given image height.

    Returns the new shifted particle image. The y-coordinate of the barycenter is
    equal to the new position.

    If clip is false, pixels which get pushed out of the picture frame, will
    appear on the other side of the picture.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    :param new_y:       new y-value for the barycenter
    :type new_y:        integer

    --- optional params ---
    :param clip:        pixels that are moved out of the picture frame are lost (default == True)
    :type clip:         boolean

    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new optical-array with shifted particle
    """
    array, data_type, slice_size = check_array_type(array, slice_size)

    # Calculate the shift.
    y_bary, _ = barycenter(array, coordinates=True, slice_size=slice_size)
    y_shift = new_y - y_bary

    new_array = np.zeros(len(array), dtype=int)
    y_dim = int(len(array) / slice_size)

    for y in range(int(len(array)/slice_size)):
        for x in range(slice_size):
            if not array[y*slice_size+x] == 0 and not array[y*slice_size+x] == '0':
                if clip:
                    # Pixels which get pushed out of the picture frame, will
                    # be clipped. !!! Loss Of Information !!!
                    if ((y_dim-1)*slice_size+x) >= ((y+y_shift) * slice_size+x) >= 0 \
                            and y_dim > (y+y_shift) >= 0:
                        new_array[(y+y_shift)*slice_size+x] = array[y*slice_size+x]
                else:
                    # Pixels which get pushed out of the picture frame, will
                    # appear on the other side of the picture.
                    new_y = (y + y_shift) % y_dim
                    new_array[new_y*slice_size+x] = array[y*slice_size+x]
    return convert_array_to_type(new_array, as_type=as_type if as_type else data_type, slice_size=slice_size)


def center_particle(array, clip=True, as_type=None, slice_size=SLICE_SIZE):
    """
    Centers a cloud particle in the image.

    If clip is false, pixels which get pushed out of the picture frame, will
    appear on the other side of the picture.

    :param array:       optical-array (particle image)
    :type array:        numpy-array (1 or 2 dimensional) or list or string

    --- optional params ---
    :param clip:        pixels that are moved out of the picture frame are lost (default == True)
    :type clip:         boolean

    :param as_type:     type of returned optical-array (1d array, 2d array, list or string)
    :type as_type:      string (values: "STRING", "LIST", "ARRAY", "ARRAY2D")

    :param slice_size:  width of the optical-array (number of diodes)
    :type slice_size:   integer

    :return:            new optical-array with centered particle
    """
    # Set x-axis image center -1 if the slice size is even
    x_center = int(slice_size / 2.0 - 0.5)
    return move_to_x(array, x_center, clip=clip, as_type=as_type, slice_size=slice_size)
