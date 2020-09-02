"""
Various functions to calculate diameters, volumes or areas of cloud particles.
"""

from math import pi, sqrt
from oap.utils import features


def xy_diameter(array):
    result = features(array)
    return result['width'], result['height']


def x_diameter(array):
    return xy_diameter(array)[0]


def y_diameter(array):
    return xy_diameter(array)[1]


def min_diameter(array):
    x, y = xy_diameter(array)
    return 2*sqrt((x*y)/pi)


def max_diameter(array):
    x, y = xy_diameter(array)
    return sqrt((x*x)+(y*y))


def sphere_volume(diameter):
    """
    Computes the volume of a sphere for a given diameter.

    :param diameter:    sphere diameter
    :type diameter:     float

    :return:            volume of the sphere (float)
    """
    r = diameter/2.0
    return (4/3)*pi*(r*r*r)


def sphere_surface(diameter):
    """
    Computes the surface area of a sphere for a given diameter.

    :param diameter:    sphere diameter
    :type diameter:     float

    :return:            surface area of the sphere (float)
    """
    r = diameter / 2.0
    return 4*pi*(r*r)


def hexprism_volume(height, diameter):
    """
    Computes the volume of a hexagonal prism.

    :param height:      height of the hexagonal prism
    :type height:       float

    :param diameter:    hexagon diameter (vertex to vertex) - equals "length of each side" * 2
    :type diameter:     float

    :return:            volume of the hexagonal prism (float)
    """
    # Edge / Side length
    e = diameter/2.0
    # Area
    area = 3/2*sqrt(3)*(e*e)
    # Volume
    volume = area*height
    return volume


def hexprism_surface(height, diameter):
    """
    Computes the surface area of a hexagonal prism.

    :param height:      height of the hexagonal prism
    :type height:       float

    :param diameter:    hexagon diameter (vertex to vertex) - equals "length of each side" * 2
    :type diameter:     float

    :return:            surface area of the hexagonal prism (float)
    """
    e = diameter / 2.0
    return (6*e*height) + (3*sqrt(3)*(e*e))
