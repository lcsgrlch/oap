
Array Modifications
===================

These functions were all developed for image preprocessing to prepare the image data for training with neural networks.

|
----

|
adjust_y
--------

    >>> oap.adjust_y(array, new_y, warning=False, as_type=None, slice_size=64)

**Description:**
    Converts the current image height (y-dimension) of the optical-array to a specific height.

    **Attention!** Particles that are too large for their new frame will be clipped off.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *new_y* : integer
        The new image height (y-dimension).

    *warning* : boolean, optional
        Gives a warning if the particle is clipped (default is False).

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array with adjusted image height (y-dimension).
|
**Examples:**
    >>> oap.print_array(array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           █ █   █ █                                                                                             |
    |                       █ █ █ █   █ █ █                                                                                           |
    |                       █ █ █     █ █ █                                                                                           |
    |                     █ █ █         █ █                                                                                           |
    |                     █ █ █       █ █ █                                                                                           |
    |                       █ █ █ █ █ █ █                                                                                             |
    |                         █ █ █ █ █                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> new_array = oap.adjust_y(array, new_y=10)
    >>> oap.print_array(new_array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           █ █   █ █                                                                                             |
    |                       █ █ █ █   █ █ █                                                                                           |
    |                       █ █ █     █ █ █                                                                                           |
    |                     █ █ █         █ █                                                                                           |
    |                     █ █ █       █ █ █                                                                                           |
    |                       █ █ █ █ █ █ █                                                                                             |
    |                         █ █ █ █ █                                                                                               |
    |                                                                                                                                 |
    |                                                                                                                                 |
    |                                                                                                                                 |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
----

|
center_particle
---------------

    >>> oap.center_particle(array, clip=True, as_type=None, slice_size=64)

**Description:**
Centers a cloud particle in the image.

*Note:* If clip is false, pixels that are pressed out of the picture frame will appear on the other side of the picture frame.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *clip* : boolean, optional
        If this is true, pixels that are moved out of the image frame will be lost (default is True).

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array with centered cloud particle.
|
----

|
clip_y
------

    >>> oap.clip_y(array, as_type=None, slice_size=64)

**Description:**
Deletes all empty image slices in the optical-array.

*Note:* If there are empty image slices between the shaded pixels, they will be deleted as well.
This can happen in rare cases when converting from grayscale to monoscale.
This would lead to a compression of the imaged cloud particle.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array without empty image slices.
|
**Examples:**
    >>> oap.print_array(array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                                                                                                                                 |
    |                                                                                                                                 |
    |                                                                                                                                 |
    |                           2 2   2 2                                                                                             |
    |                       2 2 2 2   2 2 2                                                                                           |
    |                       2 2 2     2 2 2                                                                                           |
    |                     2 2 2         1 1                                                                                           |
    |                     2 2 2       2 1 2                                                                                           |
    |                       2 2 2 2 2 1 1                                                                                             |
    |                         1 1 2 2 1                                                                                               |
    |                                                                                                                                 |
    |                                                                                                                                 |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> new_array = oap.clip_y(array)
    >>> oap.print_array(new_array, frame=True)
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
flip_x
------

    >>> oap.flip_x(array, slice_size=64)

**Description:**
Flips an optical-array in x-direction.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array that was mirrored around the y-axis.
|
**Examples:**
    >>> oap.print_array(array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                                                           1 1                                                                   |
    |                                                       1 1 1 2 2 1                                                               |
    |                                                     1 2 3 2 3 3 2 2 2 2 3 2 2 1 1                                               |
    |                                                     1 2 3 3 3 3 2 2 2 2 3 2 2 2 2 1 1 2 1 1 1                                   |
    |                                                     2 3 3 3 3 3 2 3 3 2 3 3 3 3 3 2 2 3 2 2 2 2 2 2 2   1                       |
    |                                                     2 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 2 3 2 3 3 2 2 2 3 1 1                       |
    |                                                       1 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2                       |
    |                                                           2 2 1 2 2 2 3 3 2 3 3 3 3 3 3 3 3 3 3 3 2 3 3 2                       |
    |                                                                       1 1   1 2 2 3 2 3 3 3 3 3 3 2 3 3 2                       |
    |                                                                             1 1 2 1 2 2 3 3 3 3 3 2 3 2 1                       |
    |                                                                                               1 1 1 1                           |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> new_array = oap.flip_x(array)
    >>> oap.print_array(new_array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                                                                   1 1                                                           |
    |                                                               1 2 2 1 1 1                                                       |
    |                                               1 1 2 2 3 2 2 2 2 3 3 2 3 2 1                                                     |
    |                                   1 1 1 2 1 1 2 2 2 2 3 2 2 2 2 3 3 3 3 2 1                                                     |
    |                       1   2 2 2 2 2 2 2 3 2 2 3 3 3 3 3 2 3 3 2 3 3 3 3 3 2                                                     |
    |                       1 1 3 2 2 2 3 3 2 3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 2                                                     |
    |                       2 2 2 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 1                                                       |
    |                       2 3 3 2 3 3 3 3 3 3 3 3 3 3 3 2 3 3 2 2 2 1 2 2                                                           |
    |                       2 3 3 2 3 3 3 3 3 3 2 3 2 2 1   1 1                                                                       |
    |                       1 2 3 2 3 3 3 3 3 2 2 1 2 1 1                                                                             |
    |                           1 1 1 1                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
----

|
flip_y
------

    >>> oap.flip_y(array, slice_size=64)

**Description:**
Flips an optical-array in y-direction.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array that was mirrored around the x-axis.
|
**Examples:**
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
    >>> new_array = oap.flip_x(array)
    >>> oap.print_array(new_array, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                         1 1 2 2 1                                                                                               |
    |                       2 2 2 2 2 1 1                                                                                             |
    |                     2 2 2       2 1 2                                                                                           |
    |                     2 2 2         1 1                                                                                           |
    |                       2 2 2     2 2 2                                                                                           |
    |                       2 2 2 2   2 2 2                                                                                           |
    |                           2 2   2 2                                                                                             |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
----

|
monochromatic
-------------

    >>> oap.monochromatic(array, color=1, as_type=None, slice_size=64)

**Description:**
    Converts a grayscale array into a monochromatic array.
    All shadow levels are set to a uniform value.
    The Poisson spot markings remain unchanged.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *color* : integer
        The uniform value for all shadowed pixels.

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array where all shadow layers are set to one value.
|
**Examples:**
    >>> oap.print_array(grayscale_array)
                          2 2   2 2
                      2 2 2 2   2 2 2
                      2 2 2     2 2 2
                    2 2 2         1 1
                    2 2 2       2 1 2
                      2 2 2 2 2 1 1
                        1 1 2 2 1
    >>> monochromatic_array = oap.monochromatic(grayscale_array)
    >>> oap.print_array(monochromatic_array)
                          1 1   1 1
                      1 1 1 1   1 1 1
                      1 1 1     1 1 1
                    1 1 1         1 1
                    1 1 1       1 1 1
                      1 1 1 1 1 1 1
                        1 1 1 1 1
|
----

|
monoscale
---------

    >>> oap.monoscale(array, color=1, as_type=None, slice_size=64)

**Description:**
    Converts a grayscale array into a monoscale array.
    This deletes shadow level 1 and sets the other shadow values to a uniform value.
    The Poisson spot markings remain unchanged.

    *Note:* After conversion, the optical-array may not contain any shaded pixels.
    Also, empty image slices can occur in the image.

    If the optical-array does not contain shaded pixels, the function returns None.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *color* : integer
        The uniform value for all shadowed pixels.

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array where the shadow values 2 and 3 have been set to one value and the shadow value 1 has been removed.
|
**Examples:**
    >>> oap.print_array(grayscale_array)
                          2 2   2 2
                      2 2 2 2   2 2 2
                      2 2 2     2 2 2
                    2 2 2         1 1
                    2 2 2       2 1 2
                      2 2 2 2 2 1 1
                        1 1 2 2 1
    >>> monoscale_array = oap.monoscale(grayscale_array)
    >>> oap.print_array(monoscale_array)
                          1 1   1 1
                      1 1 1 1   1 1 1
                      1 1 1     1 1 1
                    1 1 1
                    1 1 1       1   1
                      1 1 1 1 1
                            1 1
|
----

|
move_to_x
---------

    >>> oap.move_to_x(array, new_x, clip=True, as_type=None, slice_size=64)

**Description:**
Calculates the barycenter of the optical-array and shifts the cloud particle(s) in x-direction.
The x-coordinate of the new barycenter corresponds to the given value.

*Note:* If clip is false, pixels that are pressed out of the picture frame will appear on the other side of the picture frame.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *new_x* : integer
        The new x-value of the barycenter.

    *clip* : boolean, optional
        If this is true, pixels that are moved out of the image frame will be lost (default is True).

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array with shifted pixels.
|
**Examples:**
    >>> oap.print_array(array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                                                           █ █                                                                   |
    |                                                       █ █ █ █ █ █                                                               |
    |                                                     █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                               |
    |                                                     █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                   |
    |                                                     █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █   █                       |
    |                                                     █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                       |
    |                                                       █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                       |
    |                                                           █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                       |
    |                                                                       █ █   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                       |
    |                                                                             █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                       |
    |                                                                                               █ █ █ █                           |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> new_array = oap.move_to_x(array, new_x=14)
    >>> oap.print_array(new_array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |         █ █                                                                                                                     |
    |     █ █ █ █ █ █                                                                                                                 |
    |   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                                                 |
    |   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                                     |
    |   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █   █                                                                         |
    |   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                         |
    |     █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                         |
    |         █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                         |
    |                     █ █   █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                         |
    |                           █ █ █ █ █ █ █ █ █ █ █ █ █ █ █                                                                         |
    |                                             █ █ █ █                                                                             |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|
----

|
move_to_y
---------

    >>> oap.move_to_y(array, new_y, clip=True, as_type=None, slice_size=64)

**Description:**
    Calculates the barycenter of the optical-array and shifts the cloud particle(s) in y-direction.
    The y-coordinate of the new barycenter corresponds to the given value.

*Note:* If clip is false, pixels that are pressed out of the picture frame will appear on the other side of the picture frame.

**Parameters**:
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *new_y* : integer
        The new y-value of the barycenter.

    *clip* : boolean, optional
        If this is true, pixels that are moved out of the image frame will be lost (default is True).

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).
        If the value is None, the input type is again the output type.

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *optical-array* : string, list or numpy-array (1d or 2d | dtype=int)
        An optical-array with shifted pixels.
|
**Examples:**
    >>> oap.print_array(array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                           █ █   █ █                                                                                             |
    |                       █ █ █ █   █ █ █                                                                                           |
    |                       █ █ █     █ █ █                                                                                           |
    |                     █ █ █         █ █                                                                                           |
    |                     █ █ █       █ █ █                                                                                           |
    |                       █ █ █ █ █ █ █                                                                                             |
    |                         █ █ █ █ █                                                                                               |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    >>> array = oap.move_to_x(array, new_y=6)
    >>> oap.print_array(array, scales=False, frame=True)
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                                                                                                                                 |
    |                                                                                                                                 |
    |                                                                                                                                 |
    |                           █ █   █ █                                                                                             |
    |                       █ █ █ █   █ █ █                                                                                           |
    |                       █ █ █     █ █ █                                                                                           |
    |                     █ █ █         █ █                                                                                           |
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
