
Sizing Methods
==============


**Attention!**
The diameters are returned in pixels so that they are independent of the resolution of the Optical Array Probe.
If you want the actual diameter, you have to multiply the number of pixels by the resolution of the probe.

|
----

|
x_diameter
----------

    >>> oap.x_diameter(array)

**Description:**
    Measures the diameter of the particle in the x-axis (along the diode array) in image pixels.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

**Returns:**
    *x-diameter* : integer
        The measured diameter (along the diode array) of the particle in image pixels.
|
**Examples:**
    >>> oap.print_array(optical_array)
                      2 2 2 2 2
                  2 2 2 2 2 2 2 2
                  2 2 2     2 2 2
                2 2 2         1 1
                2 2 2       2 1 2
                  2 2 2 2 2 1 1
                    1 1 2 2 1
    >>> oap.x_diameter(optical_array)
    9
|
----

|
y_diameter
----------

    >>> oap.y_diameter(array)

**Description:**
    Measures the diameter of the particle in the y-axis (in flight direction) in image pixels.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

**Returns:**
    *y-diameter* : integer
        The measured diameter (in flight direction) of the particle in image pixels.
|
**Examples:**
    >>> oap.print_array(optical_array)
                      2 2 2 2 2
                  2 2 2 2 2 2 2 2
                  2 2 2     2 2 2
                2 2 2         1 1
                2 2 2       2 1 2
                  2 2 2 2 2 1 1
                    1 1 2 2 1
    >>> oap.y_diameter(optical_array)
    7
|
----

|
xy_diameter
-----------

    >>> oap.xy_diameter(array)

**Description:**
    Measures both diameters (x- and y-axis) of the particle in image pixels.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

**Returns:**
    *x-diameter, y-diameter*  : tuple of integers
        The measured x-diameter (along the diode array) and the measured y-diameter (in flight direction) of the particle. Both in image pixels.
|
**Examples:**
    >>> oap.print_array(optical_array)
                      2 2 2 2 2
                  2 2 2 2 2 2 2 2
                  2 2 2     2 2 2
                2 2 2         1 1
                2 2 2       2 1 2
                  2 2 2 2 2 1 1
                    1 1 2 2 1
    >>> oap.xy_diameter(optical_array)
    (9, 7)
|
----

|
min_diameter
------------

    >>> oap.min_diameter(array)

**Description:**
    Calculates the *Minimum Diameter* of the cloud particle. :math:`D_{min} = 2 \cdot \sqrt{\frac{x \cdot y}{pi}}`

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

**Returns:**
    *min-diameter* : float
        The calculated *Minimum Diameter* of the particle in image pixels.
|
**Examples:**
    >>> oap.print_array(optical_array)
              1 1
          1 1 1 2 2 1
        1 2 3 2 3 3 2 2 2 2 3 2 2 1 1
        1 2 3 3 3 3 2 2 2 2 3 2 2 2 2 1 1 2 1 1 1
        2 3 3 3 3 3 2 3 3 2 3 3 3 3 3 2 2 3 2 2 2 2 2 2 2   1
        2 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 2 3 2 3 3 2 2 2 3 1 1
          1 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2
              2 2 1 2 2 2 3 3 2 3 3 3 3 3 3 3 3 3 3 3 2 3 3 2
                          1 1   1 2 2 3 2 3 3 3 3 3 3 2 3 3 2
                                1 1 2 1 2 2 3 3 3 3 3 2 3 2 1
                                                  1 1 1 1
    >>> oap.min_diameter(optical_array)
    19.44613444328572
|
----

|
max_diameter
------------

    >>> oap.max_diameter(array)

**Description:**
    Calculates the *Maximum Diameter* of the cloud particle. :math:`D_{max} = \sqrt{x^2 + y^2}`

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

**Returns:**
    *max-diameter* : float
        The calculated *Maximum Diameter* of the particle in image pixels.
|
**Examples:**
    >>> oap.print_array(optical_array)
              1 1
          1 1 1 2 2 1
        1 2 3 2 3 3 2 2 2 2 3 2 2 1 1
        1 2 3 3 3 3 2 2 2 2 3 2 2 2 2 1 1 2 1 1 1
        2 3 3 3 3 3 2 3 3 2 3 3 3 3 3 2 2 3 2 2 2 2 2 2 2   1
        2 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 2 3 2 3 3 2 2 2 3 1 1
          1 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2
              2 2 1 2 2 2 3 3 2 3 3 3 3 3 3 3 3 3 3 3 2 3 3 2
                          1 1   1 2 2 3 2 3 3 3 3 3 3 2 3 3 2
                                1 1 2 1 2 2 3 3 3 3 3 2 3 2 1
                                                  1 1 1 1
    >>> oap.max_diameter(optical_array)
    29.154759474226502
|
----

|
area_ratio
----------

    >>> oap.area_ratio(array)

|
----

|
sphere_volume
-----------------

    >>> oap.sphere_volume(diameter)

**Description:**
    Computes the volume of a sphere for a given diameter.

**Parameters:**
    *diameter* : float
        The diameter of the sphere.

**Returns:**
    *volume* : float
        The calculated volume of the sphere.
|
**Examples:**
    >>> oap.sphere_volume(10.5)
    606.1310326019807
|
----

|
sphere_surface
-----------------

    >>> oap.sphere_surface(diameter)

**Description:**
    Computes the surface area of a sphere for a given diameter.

**Parameters:**
    *diameter* : float
        The diameter of the sphere.

**Returns:**
    *surface area* : float
        The calculated surface area of the sphere.
|
**Examples:**
    >>> oap.sphere_surface(10.5)
    346.3605900582747
|
----

|
hexprism_volume
-----------------

    >>> oap.hexprism_volume(height, diameter)

**Description:**
    Computes the volume of a hexagonal prism for a given height and a given diameter.

**Parameters:**
    *height* : float
        The height of the hexagonal prism.

    *diameter* : float
        The vertex to vertex diameter of the hexagon, which is equal to the side length times two.

**Returns:**
    *volume* : float
        The calculated volume of the hexagonal prism.
|
**Examples:**
    >>> oap.hexprism_volume(height=14.5, diameter=5.25)
    259.5843489609184
|
----

|
hexprism_surface
-----------------

    >>> oap.hexprism_surface(height, diameter)

**Description:**
    Computes the surface area of a hexagonal prism for a given height and a given diameter.

**Parameters:**
    *height* : float
        The height of the hexagonal prism.

    *diameter* : float
        The vertex to vertex diameter of the hexagon, which is equal to the side length times two.

**Returns:**
    *surface area* : float
        The calculated surface area of the hexagonal prism.
|
**Examples:**
    >>> oap.hexprism_surface(height=14.5, diameter=5.25)
    264.1797377877129
