
Globals
=======

|
Particle Types
--------------
Particle types are defined as single bytes in the oap library.
They can be used to classify optical-arrays.
The following particle types are already defined:
::
    UNDEFINED = b'u'    # Not yet classified
    INDEFINABLE = b'i'  # Not possible to classify
    ERRONEOUS = b'e'    # Artefacts or erroneous images
    SPHERE = b's'       # Spherical particles
    COLUMN = b'c'       # Column-like particles
    ROSETTE = b'r'      # Rosettes
    DENDRITE = b'd'     # Dendrites
    PLATE = b'p'        # Plates
|
**Example:**
::
    >>> import oap
    >>> oap.COLUMN
    b'c'
    >>> array, p_type = oap.read_oap_file("example01.oap")
    >>> oap.print_array(array)
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
    >>> p_type == oap.COLUMN
    True
If the given particle types are not sufficient, you can use unused bytes to define your own types. For example:
::
    >>> oap.array_as_oap_file(array, "example02", p_type=b'x')
    >>> array, p_type = oap.oap.read_oap_file("example02.oap")
    >>> p_type
    b'x'
