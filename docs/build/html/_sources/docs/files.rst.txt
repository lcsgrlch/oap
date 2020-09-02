
File Methods
============

The **oap** library contains a couple of Python functions to save optical-arrays permanently or convert them to PNGs.
There are also some helper functions to simplify the work with a great number of files.

|
----

|
array_as_oap_file
-----------------

    >>> oap.array_as_oap_file(array, filename, p_type=oap.UNDEFINED,
    ...                       file_extension=".oap")

**Description:**
    Stores an optical-array with associated particle type as a binary file (oap-file).

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *filename* : string
        File path *without* file extension.

    *p_type* : char, optional
        Particle Type of the cloud particle (default is b'u').

    *file_extension* : string, optional
        Determines the file extension (default is ".oap").
|
**Examples:**
    >>> oap.array_as_oap_file(array, filename="particles/column01",
    ...                       p_type=oap.COLUMN)
|
----

|
array_as_png
------------

    >>> oap.array_as_png(array, filename=None, scale=1, slice_size=64)

**Description:**
    Creates a PNG image of an optical-array. If the file name is not equal to None, the image is saved.
    Otherwise, the image is saved in random access memory only.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *filename* : string, optional
        File path *without* file extension.

    *scale* : integeer, optional
        The image scale (default is 1).

    *slice_size* : integer, optional
        The width of the optical-array (number of diodes). Only necessary, if the optical-array is one dimensional (default is 64).

**Returns:**
    *png image* : PIL.Image.Image
        A PIL image object that is stored in memory.

|
**Examples:**
    >>> png_image = oap.array_as_png(array, filename="imgages/column01", scale=3)
    >>> png_image
    <PIL.Image.Image image mode=L size=192x21 at 0x27A37DA7988>
|
----

|
filepaths
---------

    >>> oap.filepaths(directory, exclude=None, include=None,
    ...               p_types=None, file_extension=OAP_FILE_EXTENSION)

**Description:**
    Finds all files with the specified file extension in a directory and returns a list of file paths.
    It is possible to search only specific folders, or exclude folders from the search.

**Parameters:**
    *directory* : string
        The directory to be searched.

    *exclude* : list of strings, optional
        A list of folders to be excluded (default is None).

    *include* : list of strings, optional
        A list of specific subfolders to be searched exclusively (default is None).

    *p_types* : list of chars
        A list of the particle types you are looking for (default is None).

        * This should only be used if the searched files are oap-files!

    *file_extension* : string, optional
        The wanted file extension (default is ".oap")

**Returns:**
    A list of file paths.
|
**Examples:**
    >>> files = oap.filepaths("tests", include=["data"])
    ['tests\\data\\array01.oap', 'tests\\data\\array02.oap', 'tests\\data\\array03.oap', 'tests\\data\\array04.oap']
|
----

|
read_particle_type
------------------

    >>> oap.read_particle_type(filename)

**Description:**
    Reads and returns the particle type of an oap file.

**Parameters:**
    *filename* : string
        File path *with* file extension.

**Returns:**
    *particle type* : char
|
**Examples:**
    >>> p_type = oap.read_particle_type("particles/column01.oap")
    >>> p_type
    b'c'
    >>> p_type == oap.COLUMN
    True
|
----

|
read_oap_file
-------------

    >>> oap.read_oap_file(filename, as_type="array2d", slice_size=64)

**Description:**
    Loads a binary oap-file and returns the optical-array and the corresponding stored particle type.

**Parameters:**
    *array* : string, list or numpy-array (1d or 2d | dtype=int)
        The optical-array (particle image).

    *filename* : string
        File path *with* file extension.

    *as_type* : string, optional
        The type of the returned optical-array - string, list or numpy-array (1d or 2d | dtype=int).

        * Possible values: None, "str", "string", "list", "array", "array2d"

    *slice_size* : integer, optional
        The width of the optical-array (default is 64).

**Returns:**
    *optical-array, particle type* : tuple
        The optical-array and the corresponding particle type.
|
**Examples:**
    >>> array, p_type = oap.read_oap_file("particles/column01.oap")
    >>> p_type
    b'c'
    >>> p_type == oap.COLUMN
    True
    >>> oap.print_array(array)
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
