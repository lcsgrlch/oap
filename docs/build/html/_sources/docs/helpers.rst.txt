
Helper Functions
================

|
barycenter
----------

    >>> oap.barycenter(array, coordinates=True, slice_size=64)

**Description:**
    Calculates the barycenter of an optical-array. Returns the barycenter as integer indices or as exact floating point numbers.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *coordinates* : boolean, optional
        If true, the computed values are rounded to the nearest integer value so that they can be used as indices for an array (default is True).

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *barycenter* : tuple (integers or floats)
        The y- and the x-value of the barycenter.
|
**Examples:**
    >>> array, _ = oap.read_oap_file("example01.oap", as_type="array2d")
    >>> oap.print_array(array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           2 2   2 2                                                                                             |
    |                       2 2 2 2   2 2 2                                                                                           |
    |                       2 2 2     2 2 2                                                                                           |
    |                     2 2 2         1 1                                                                                           |
    |                     2 2 2       2 1 2                                                                                           |
    |                       2 2 2 2 2 1 1                                                                                             |
    |                         1 1 2 2 1                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> y_bary, x_bary = oap.barycenter(array)
    >>> print("y:", y_bary, "x:", x_bary)
    y: 3 x: 14
    >>> type(array)
    <class 'numpy.ndarray'>
    >>> array.ndim
    2
    >>> array[oap.barycenter(array)] = 9
    >>> oap.print_array(array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           2 2   2 2                                                                                             |
    |                       2 2 2 2   2 2 2                                                                                           |
    |                       2 2 2     2 2 2                                                                                           |
    |                     2 2 2   9     1 1                                                                                           |
    |                     2 2 2       2 1 2                                                                                           |
    |                       2 2 2 2 2 1 1                                                                                             |
    |                         1 1 2 2 1                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
