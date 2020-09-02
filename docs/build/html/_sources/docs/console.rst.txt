
Console Output
==============

|
print_array
-----------

    >>> oap.print_array(array, frame=False, scales=True, slice_size=64)

**Description:**
    Prints an optical-array to the console output.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *frame* : boolean, optional
        If true, display a picture frame around the array (default is False).

    *scales* : boolean, optional
        If true, show pixel scales (default is True).

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes) only necessary, if optical-array is one dimensional (default is 64).
|
**Examples:**
    >>> oap.print_array(optical_array)
                              2 2   2 2
                          2 2 2 2   2 2 2
                          2 2 2     2 2 2
                        2 2 2         1 1
                        2 2 2       2 1 2
                          2 2 2 2 2 1 1
                            1 1 2 2 1
    >>> oap.print_array(optical_array, scales=False)
                              █ █   █ █
                          █ █ █ █   █ █ █
                          █ █ █     █ █ █
                        █ █ █         █ █
                        █ █ █       █ █ █
                          █ █ █ █ █ █ █
                            █ █ █ █ █
    >>> oap.print_array(optical_array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           2 2   2 2                                                                                             |
    |                       2 2 2 2   2 2 2                                                                                           |
    |                       2 2 2     2 2 2                                                                                           |
    |                     2 2 2         1 1                                                                                           |
    |                     2 2 2       2 1 2                                                                                           |
    |                       2 2 2 2 2 1 1                                                                                             |
    |                         1 1 2 2 1                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
----

|
print_separator
---------------

    >>> oap.print_separator(separator='-', slice_size=64)

**Description:**
    Prints a simple separator for particle previews to the console output.
    The width of the separator refers to the number of diodes (slice size).

**Parameters:**
    *separator* : char, optional
        The symbol of the separator.

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes).
