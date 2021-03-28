
Part 1: Decompress an imagefile of an Optical Array Probe
=========================================================

The first thing you might want to try is to decompress and output your own data.
The following code decompresses a sample image file and then prints the first 100 images in the console.
::
    import oap

    images = []
    oap.decompress("Imagefile20200830120000", images=images)

    for image in images[:100]:
        oap.print_array(image)
        oap.print_separator()

If you collect data for the training of a neural network or another classifier, you can save single images in a self-developed file format (.oap) to be able to load and edit them later.
As an example we recognized a rosette in an image and want to save it with the corresponding particle type.
::
    oap.array_as_oap_file(image, filename="rosette01", p_type=oap.ROSETTE)

The particle image is saved with the name "rosette02.oap".
If you want to load the image again later, you can do this as follows:
::
    >>> array, p_type = oap.read_oap_file("rosette01.oap")
    >>> oap.print_array(array)
                          1 2
                          2 2 2
                        1 2 3 3
                          3 3 3 1
    2 3 3 2               2 3 3 3
    3 3 3 3 3 1           1 3 3 3 1 1 2 2 1
    1 3 3 3 3 3 3 2 1       2 3 3 3 3 2 3 1
        3 3 3 3 3 3 3 2     2 3 3 3 3 3 3
            3 3 3 3 3 3 2   2 3 3 3 3 3 3
                1 1 3 3 2 2 3 3 3 3 3 3 3 1
        1 1 2 2 1 1 2 2 2 3 3 3 3 3 3 3 3 2 1 1   1
      1 3 3 3 3 3 2 2 2 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 1
      2 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 3 2 2
      1 3 3 3 3 2 1 3 1 1 1   3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 3 2 1
        2 1 1                 2 3 3 3 3 3 3 3 3 3 3 3 3 3 2 3 1
                              2 3 3 3       2 3 3 3 3 2 3 2 2 1
                              2 3 3 3       1 2 3 3 3 2 2 2 3 1
                            1 2 3 2 1               2 2 3 2 3 2
                            2 2 3 3                     2 2 3 1
                            2 3 3 3
                            2 3 3 2
                            1 2 2

If you want to save this image in PNG format, you can do it with the following command:
::
    oap.array_as_png(array, "rosette01")

This method creates an image in PNG format with the name "rosette01.png".