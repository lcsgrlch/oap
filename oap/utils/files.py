"""
Various functions for file export and import of optical arrays.
Also some helper functions to simplify the work with a great number of files.
"""

import os
import numpy as np
from PIL import Image
from binascii import hexlify

from oap.__conf__ import COLOR, DEFAULT_TYPE, OAP_FILE_EXTENSION, UNDEFINED, SLICE_SIZE
from oap.utils.bytes import read_particle_type


def array_as_oap_file(array, filename, p_type=UNDEFINED, file_extension=OAP_FILE_EXTENSION):
    """
    Stores an optical array with associated particle type as a binary file.

    :param array:           optical array (particle image)
    :type array:            string, list or numpy array (1d or 2d | dtype=int)

    :param filename:        path to oap-file
    :type filename:         string

    :param p_type:          particle type
    :type p_type:           char

    :param file_extension:  file type
    :type file_extension:   string
    """
    with open(filename + file_extension, "wb") as f:

        if type(array).__module__ == np.__name__:
            if array.ndim == 2:
                array = np.ravel(array)

        # header_size = 1
        f.write(p_type)

        for i in range(len(array)):
            byte = chr(int(array[i]))
            f.write(byte.encode("utf-8"))
        f.close()


def array_as_png(array, filename=None, scale=1, slice_size=SLICE_SIZE):
    """
    Creates a PNG image of an optical array. If the file name is not equal to None, the image is saved.
    Otherwise, the image is saved in random access memory only.

    :param array:       optical array (particle image)
    :type array:        string, list or numpy array (1d or 2d | dtype=int)

    :param filename:    path to png-file
    :type filename:     string

    :param scale:       image scale
    :type scale:        integer

    :param slice_size:  width of the optical array (number of diodes)
    :type slice_size:   integer
    """
    # If the optical array is a 2 dimensional numpy array,
    # flatten it and update the slice size.
    if type(array).__module__ == np.__name__:
        if array.ndim == 2:
            slice_size = array.shape[1]
            array = np.ravel(array)

    data = np.zeros(len(array), dtype=np.uint8)
    for i in range(len(array)):
        data[i] = COLOR[int(array[i])]
    data = data.reshape(int(len(array) / slice_size), slice_size)

    image = Image.fromarray(data)
    image = image.resize((scale * slice_size, scale * int(len(array) / slice_size)))
    if filename:
        image.save(filename + ".png", "PNG")
    return image


def filepaths(directory, exclude=None, include=None, p_types=None, file_extension=OAP_FILE_EXTENSION):
    """
    Finds all files with the specified file extension in a directory and returns a list of file paths.
    It is possible to search only specific folders, or exclude folders from the search.

    :param directory:       path to directory
    :type directory:        string

    :param exclude:         list of folders to be excluded
    :type exclude:          list of strings

    :param include:         list of specific subfolders to be searched exclusively
    :type include:          list of strings

    :param p_types:         list of the particle types you are looking for
    :type p_types:          list of strings

    :param file_extension:  file type
    :type file_extension:   string

    :return:                list of file paths
    """

    if include is None:
        include = []
    if exclude is None:
        exclude = []
    if p_types is None:
        p_types = []
    files = [os.path.join(root, f)
             for root, _, files in os.walk(directory)
             if not any(x in exclude for x in root.split(os.sep))
             and (bool(len(include)) == bool(any(x in include for x in root.split(os.sep))))
             for f in files if f.endswith(file_extension)]

    if len(p_types):
        files = [f for f in files if (bool(len(p_types)) == bool(read_particle_type(f) in p_types))]
    return files


def read_oap_file(filename, as_type=DEFAULT_TYPE, slice_size=SLICE_SIZE):
    """
    Loads a binary oap file and returns the optical array and the corresponding stored particle type.

    :param filename:    path to oap-file
    :type filename:     string

    :param as_type:     data type of the returned optical array ("array", "array2d", "list", "string")
    :type as_type:      string

    :param slice_size:  width of the optical array (number of diodes)
    :type slice_size:   integer

    :return:            tuple - (optical-array : string, list or numpy-array (1d or 2d | dtype=int),
                                 particle-type : char)
    """
    with open(filename, "rb") as f:

        # Binary particle header.
        header_size = 1     # int(hexlify(f.read(1)), 16)
        p_type = f.read(header_size)

        byte = f.read(1)

        if as_type.upper() == "STRING" or as_type.upper() == "STR":
            array = ""
            while byte:
                byte = int(hexlify(byte), 16)
                array += str(byte)
                byte = f.read(1)
            f.close()
            return array, p_type

        elif as_type.upper() == "LIST":
            array = []
            while byte:
                byte = int(hexlify(byte), 16)
                array.append(byte)
                byte = f.read(1)
            f.close()
            return array, p_type

        elif as_type.upper() == "ARRAY":
            file_size = os.stat(filename).st_size - header_size
            array = np.zeros(file_size, dtype=int)
            i = 0
            while byte:
                byte = int(hexlify(byte), 16)
                array[i] = byte
                byte = f.read(1)
                i += 1
            f.close()
            return array, p_type

        elif as_type.upper() == "ARRAY2D" or as_type.upper() == "2DARRAY":
            file_size = os.stat(filename).st_size - header_size
            array = np.zeros((int(file_size / slice_size), slice_size), dtype=int)
            y = 0
            x = 0
            while byte:
                byte = int(hexlify(byte), 16)
                array[y][x] = byte
                byte = f.read(1)
                x += 1
                if x == 64:
                    x = 0
                    y += 1
            f.close()
            return array, p_type
