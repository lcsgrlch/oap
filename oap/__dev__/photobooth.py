"""
Optical Array Probe Particle Image Simulation.

Author:         Lucas Tim Grulich
Created:        August 2018
Last Update:    01. August 2019
"""

from oap.__conf__ import SLICE_SIZE
# from oap.utils.sizing import particle_radius

import numpy as np
import random as rnd

# from scipy.misc import imread
from matplotlib.pyplot import imread
from LightPipes import Begin, Fresnel, Intensity, mm, um, nm


def load_png_as_normalized_array(filename, alpha=0.0):
    """
    Loads a PNG image and converts it to a nomralized 2d array.

    :param filename:    path to the png image file
    :type filename:     string

    --- optional params ---
    :param alpha:       addition to the shadowlevel, which is initially 0.0
    :type alpha:        float (between 0.0 and 1.0)

    :return:            numpy float array (2 dimensional)
    """

    # ToDo: write good png import
    # Import PNG as numpy array -> also flattens RGB values.
    image = imread(filename)

    array = np.ones(image.shape[:2])
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if sum(image[i, j]) == 4:
                pass
            else:
                array[i, j] = 0

    # Normalize array
    # array *= (1.0/array.max())

    # Reducing the shadow intensity.
    array = array+alpha
    # Clipping the normalized array
    return np.clip(array, 0.0, 1.0)


def fresnel_diffraction(array, Z, wavelength=658.0, resolution=15.0, diodes=SLICE_SIZE):
    """
    Changes the particle shadow depending on the distance Z to the
    Depth Of Field (DOF) (or sometimes Object Plane) by calculating
    the Fresnel Diffraction. The Object Plane is the area in which
    a cloud particle is sharply recorded.

    :param array:       image as numpy array
    :type array:        numpy float array (2 dimensional)

    :param Z:           distance to the object plane
    :type Z:            float

    --- optional params ---
    :param wavelength:  laser wavenlength in nanometers
    :type wavelength:   float

    :param resolution:  single diode resolution in micrometers
    :type resolution:   float

    :param diodes:      number of diodes in virtual diode array
    :type diodes:       integer

    :return:            numpy float array (2 dimensional)
    """
    if len(array) != len(array[0]):
        return None
    size = len(array)
    if size % diodes != 0:
        return None

    # --- Calculation of the dimensionless distance to the object plane --------
    # r = particle_radius(smile_for_the_camera(image, dim="1D"))
    # if r == 0:
    #   return None

    # Radius is in pixels and has to be changed to millimeter
    # r *= (resolution * 0.001)

    # Dimensionless distance
    # Zd = lambda *  |Z| / r^2
    # Zd = (Z / (r*r)) * (wavelength * 1e-6) # Wavelength in millimeters

    # Distance in millimeter
    # |Z| = (Zd * r^2) / lambda
    # Z = (Zd * (r*r)) / (wavelength * 1e-6) # Wavelength in millimeters

    # The field has light reflecting walls, which will influence the actual image. Therefore,
    # use a grid dimension, which is 3 times the actual size and crop the image afterwards.
    grid_dimension = 3*size
    # For example: CIPgs sample area -> 15um single diode resolution
    sample_area = ((resolution*grid_dimension) / (size/diodes)) * um

    field = Begin(sample_area, wavelength*nm, grid_dimension)
    for y in range(size):
        for x in range(size):
            field[y+size][x+size] = complex(array[x][y], 0)
    # also possible: Forvard / Fresnel
    field = Fresnel(Z*mm, field)
    field = Intensity(0, field)
    # Crop the image.
    return np.array(field)[size:2*size,
                           size:2*size]


def _shadow_level(kernel, threshold, sensitivity):
    """
    Calculates the greyscale shadow level for a given kernel,
    the diode threshold and the diode sensitivity.

    :param kernel:      pooling kernel for down scaling
    :type kernel:       float array (2 dimensional)

    :param threshold:   thresholds for light intensity (determines the shadowlevel)
    :type threshold:    list or tuple (len == 3) descending order

    :param sensitivity: diode sensitivity
    :type sensitivity:  float

    :return:            shadowlevel (integer between 0 and 3)
    """
    light_intensity = 0.0
    for y in range(len(kernel)):
        for x in range(len(kernel[0])):
            light_intensity += kernel[y][x]
    # Normalizing the shadowlevel with kernel size
    light_intensity /= (len(kernel)*len(kernel[0]))
    if   light_intensity > (threshold[0] + sensitivity):
        return 0
    elif light_intensity > (threshold[1] + sensitivity):
        return 1
    elif light_intensity > (threshold[2] + sensitivity):
        return 2
    else:
        return 3


def smile_for_the_camera(array, threshold=[0.65, 0.5, 0.35], lb=-0.000001, ub=0.000001,
                         slicerate=1.0, triangular=True, clip=True, dim="2D", diodes=SLICE_SIZE):
    """
    Simulation of the 1-dimensional recording of ice particles with an
    optical array probe. The slice rate of the recording is adjustable.

    :param array:       normalzed particle image as array
    :type array:        numpy array (2 dimensional)

    --- optional params ---
    :param threshold:   thresholds for light intensity (determines the shadowlevel)
    :type threshold:    list or tuple (len == 3) descending order

    :param lb:          lower border for randomized diode sensitivity
    :type lb:           float (negative value)

    :param ub:          upper border for randomized diode sensitivity
    :type ub:           float (positive value)

    :param slicerate:   slice rate of image capturing (stretches or compresses)
    :type slicerate:    float

    :param triangular:  uses the triangular random function for diode sensitivity
    :type triangular:   boolean

    :param clip:        clips array in y-dimension (default == True)
    :type clip:         boolean

    :param dim:        dimension of output array (default == "2D", optional == "1D")
    :type dim:         string

    :param diodes:      number of diodes in virtual diode array
    :type diodes:       integer

    :return:            numpy array (1 dimensional)
    """
    # The given scalar field size must be divisible by 64.
    if len(array[0]) % diodes != 0:
        return None

    kernel_size = len(array[0]) / diodes

    # Calculate the step size for the given slice rate.
    h = len(array) / (slicerate*len(array))

    # Choose a random sensitivity for the diodes.
    if triangular:
        sensitivity = np.random.triangular(lb, 0.0, ub, diodes)
    else:
        sensitivity = [rnd.uniform(lb, ub) for _ in range(diodes)]

    new_array = []
    for y in np.arange(0.0, diodes, h):

        diode_array = np.zeros(diodes, dtype=int)
        z = int(y) if int(round(y)) >= diodes else int(round(y))

        for x in range(diodes):
            kernel = array[int(z*kernel_size):int(z*kernel_size+kernel_size),
                           int(x*kernel_size):int(x*kernel_size+kernel_size)]
            diode_array[x] = _shadow_level(kernel, threshold, sensitivity[x])

        # Don't append empty slices.
        if max(diode_array) or not clip:
            new_array.append(diode_array)
    if dim is "1D":
        return np.ravel(new_array)
    return np.array(new_array)
