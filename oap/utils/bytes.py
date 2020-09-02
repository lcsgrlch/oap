"""
Various functions for reading and changing bytes from files.
"""


def read_particle_type(filename):
    """
    Reads and returns the particle-type of an oap file.

    :param filename:    path to file
    :type filename:     string
    """
    return read_bytes(filename=filename, offset=0, number=1)


def read_bytes(filename, offset, number):
    """
    Reads specific bytes of a binary file.

    :param filename:    path to file
    :type filename:     string

    :param offset:      start reading at offset
    :type offset:       integer

    :param number:      number of bytes
    :type number:       integer

    :return:            byte string
    """
    with open(filename, "rb") as f:
        f.seek(offset)
        byte_string = f.read(number)
        f.close()
        return byte_string


def modify_bytes(filename, offset, byte_string):
    """
    Modifies specific bytes in a binary file.

    :param filename:    path to file
    :type filename:     string

    :param offset:      writing at offset
    :type offset:       integer

    :param byte_string: byte to be written
    :type byte_string:  char
    """
    with open(filename, "r+b") as f:
        f.seek(offset)
        f.write(byte_string)
        f.close()
