
Part 2: The Imagefile and the OpticalArray Object
=================================================

This is just a brief tutorial to introduce the two classes Imagefile and OpticalArray.
You can find more details about the classes in the documentation and in further tutorials.
First, an object of the Imagefile class is initialized with the path to an imagefile.
::
    from oap import Imagefile

    imagefile = Imagefile("Imagefile_CIP Grayscale_20200830120000")

You can also search for particle types. At the current state the two particle types columns and rosettes are supported.
::
    imagefile.classify()

Plot the number of particles per second of day for all particles recorded.
::
    imagefile.plot()

Plot the number of rosettes per second of day.
::
    imagefile.plot(r=(0.5, 1))

Get all optical arrays containing particles of size 100 to 200 micrometers (area ratio) that were recorded between flight seconds 20000 and 22000.
::
    array_list = imagefile.get_arrays(timespan=(20000, 22000),
                                      area_ratio=(100, 200))

    # print particle images
    for array in array_list:
        array.print()
