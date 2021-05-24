"""
Short blender script for rendering objects for different rotations, locations and scales.
Developed for the "ParticleRayTracer.blend" file.


--- How to use ---

In Blender:
1. Enable layer 1 (camera) and the layer corresponding to a cloud particle.
2. Make sure the cloud particle uses the OpaqueBlenderRender material and the selected
   renderer is the Blender Renderer.
3. (Optional) Change the resolution in pixels.

In this script:
4. Add or delete particles ####### the variable PARTICLE (in this script) to the name of your selected cloud particle.
5. Change the output directory DIRECTORY.
6. (Optional) Make sure folder name fits to the pixel resolution.

Back to Blender:
7. Reload and Run Script.



Author:  Lucas Grulich
Date:    October 2017
Updated: September 2018
"""

import bpy
import bmesh
import numpy as np
from math import radians, sqrt, pi
from os.path import join

# Add the object name, the object layer and the volume and area (if available) to the tupel-list for rendering!
PARTICLES = [("Sphere", 4, 0, 0),  # Spherical Particles
             ("Indefinable01", 5, 6.536, 64.34615), ("Indefinable02", 6, 27.734, 173.5154),  # Indefinable Particles
             ("Indefinable03", 7, 85.092, 301.0821), ("Indefinable04", 8, 32.278, 90.14075),
             ("Indefinable05", 9, 2.4837, 57.73505),
             ("CombinedColumns01", 11, 59.466, 153.7492), ("CombinedColumns02", 12, 182.11, 441.1845),  # Rosettes
             ("CombinedColumns03", 13, 55.304, 151.1618), ("CombinedColumns04", 14, 82.806, 230.1902),
             ("CombinedColumns05", 19, 90.068, 238.5426),
             ("HollowColumn01", 10, 2.0674, 0), ("Bullet01", 15, 2.4627, 0),
             ("Bullet02", 16, 2.7405, 0)]  # Columns and Bullets
"""
Experimental Particles:
PARTICLES = [("Graupel01", 2, 4.3795, 13.64108), ("Plate01", 3, 0, 0), ("CappedColumn01", 17, 0, 0), ("Dendrite01", 18, 0, 0)]
"""

RESOLUTION = "128"
DIRECTORY = "C:/Monoscale_" + RESOLUTION + "px/"


def hexagon_surface(height, diameter):
    """
    Computes the surface area of a hexagonal structure.
    """
    a = diameter / 2.0
    return (6 * a * height) + (3 * sqrt(3 * (a * a)))


def render_scene(fname, directory, scene="Scene"):
    fpath = join(directory, fname + ".png")
    bpy.data.scenes[scene].render.filepath = fpath
    bpy.ops.render.render(write_still=True)


def reset_object(obj):
    """
    Reset objects rotation, location and scale.
    (x, y, z) with axis-color (red, green, blue)
    """
    obj.rotation_euler = (0, 0, 0)
    obj.location = (0, 0, 0)
    obj.scale = (1, 1, 1)


def disable_all_layers():
    """
    Diables all the render layers.
    """
    bpy.context.scene.layers[0] = True
    for i in range(1, len(bpy.context.scene.layers)):
        bpy.context.scene.layers[i] = False


def scale_and_rotate_object(obj, scale, volume, area, X, Y, Z, directory, render=False):
    """
    Scales and rotates an object. The distance and the scale are fixed,
    otherwise the object would maybe touch the optical array in the scene.
    """
    obj.scale = scale
    obj.location = (0, 0, 0)

    v = volume * scale[0] * scale[1] * scale[2]
    a = area * scale[0] * scale[1]

    for x in X:
        for y in Y:
            for z in Z:

                obj.rotation_euler = (radians(x), radians(y), radians(z))

                if render:
                    fname = obj.name + "_s{:05.2f}".format(scale[0])
                    fname += "_v{:011.5f}".format(v) + "_a{:011.5f}".format(a)
                    fname += "_x{:03d}".format(x) + "_y{:03d}".format(y) + "_z{:03d}".format(z)
                    render_scene(fname, directory)


def scale_transform_and_rotate_object(obj, width, length, volume, directory, render=False):
    """
    Scales, transforms and rotates an object. The start location is fixed,
    otherwise the object can touch the optical array in the scene.
    """
    obj.scale = (width, width, length)
    obj.location = (0, 0, 0)

    v = volume * width * width * length
    a = hexagon_surface(length, width * 2)

    for x in range(0, 50, 10):
        # Give it a small tilt in the beginning, since total
        # linear images are unexpactable in real cloud data.
        for y in range(2, 90, 5):
            for z in range(0, 50, 10):

                obj.rotation_euler = (radians(x), radians(y), radians(z))

                if render:
                    fname = obj.name + "_l{:05.2f}".format(length) + "_w{:05.2f}".format(width)
                    fname += "_v{:011.5f}".format(v) + "_a{:011.5f}".format(a)
                    fname += "_x{:03d}".format(x) + "_y{:03d}".format(y) + "_z{:03d}".format(z)
                    render_scene(fname, directory)


def scale_and_transform_object(obj, directory, render=False):
    """
    Scales and transforms an object in dependence of its radius.
    """
    for r in np.arange(1, 30, 0.5):
        obj.scale = (r, r, r)

        v = (4 / 3) * r * r * r * pi
        a = 4 * r * r * pi

        # Change slightly the x and z postion. It changes the
        # rendered image, because of the low resolution.
        # This effect is more noticeable for smaller radii.
        # Since the rendering technique is orthographic a change
        # in the y position, won't change the resulting image
        for x in np.arange(0, 10, 0.5):
            for z in np.arange(0, 10, 0.5):
                obj.location = ((x / 10.0), 0, (z / 10.0))

                if render:
                    fname = obj.name + "_r{:05.2f}".format(r)
                    fname += "_v{:011.5f}".format(v) + "_a{:011.5f}".format(a)
                    fname += "_x{:05.2f}".format(x) + "_z{:05.2f}".format(z)
                    render_scene(fname, directory)


if __name__ == "__main__":

    for particle, layer_index, volume, area in PARTICLES:

        # Disbale all layers but the camera layer 0
        disable_all_layers()
        directory = DIRECTORY + particle
        obj = bpy.data.objects[particle]
        # Set the corresponding layer to True
        bpy.context.scene.layers[layer_index] = True

        if particle == "Sphere":
            print("\nStart Rendering Spherical Objects...\n")
            scale_and_transform_object(obj, directory, True)
            reset_object(obj)

        elif particle == "HollowColumn01":
            print("\nStart Rendering Hollow Columns...\n")
            configurations = [(1, 10), (1, 20), (1, 30), (1, 40),
                              (2, 15), (2, 20), (2, 30), (2, 40),
                              (3, 15), (3, 20), (3, 25), (3, 30),
                              (4, 15), (4, 20), (4, 25), (4, 30),
                              (5, 25), (5, 30), (5, 40)]
            # Start Rendering for every configuration
            for width, length in configurations:
                scale_transform_and_rotate_object(obj, width, length, volume, directory, True)
                reset_object(obj)

        elif particle == "Bullet01":
            print("\nStart Rendering Bullets...\n")
            configurations = [(1, 10), (1, 15),
                              (2, 10), (2, 15), (2, 20), (2, 25),
                              (3, 15), (3, 20), (3, 25), (3, 30),
                              (4, 15), (4, 20), (4, 25), (4, 30),
                              (5, 25), (5, 30), (5, 40)]
            # Start Rendering for every configuration
            for width, length in configurations:
                scale_transform_and_rotate_object(obj, width, length, volume, directory, True)
                reset_object(obj)

        elif particle == "Bullet02":
            print("\nStart Rendering Bullets...\n")
            configurations = [(1, 10), (1, 15),
                              (2, 10), (2, 15), (2, 20), (2, 25),
                              (3, 15), (3, 20), (3, 25), (3, 30),
                              (4, 15), (4, 20), (4, 25), (4, 30),
                              (5, 25), (5, 30), (5, 40)]
            # Start Rendering for every configuration
            for width, length in configurations:
                scale_transform_and_rotate_object(obj, width, length, volume, directory, True)
                reset_object(obj)

        else:
            if particle == "CombinedColumns01":
                print("\nStart Rendering Combined Bullets...\n")
                configurations = [(i, i, i) for i in np.arange(1.5, 5.0, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "CombinedColumns02":
                print("\nStart Rendering Combined Hollow Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 3.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "CombinedColumns03":
                print("\nStart Rendering Combined Four Branches...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 5.0, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "CombinedColumns04":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 4.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "CombinedColumns05":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(2.0, 4.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Graupel01":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(2.0, 27, 1)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Indefinable01":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 9.0, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Indefinable02":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 6.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Indefinable03":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(0.50, 4.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Indefinable04":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 9.5, 0.5)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Indefinable05":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(i, i, i) for i in np.arange(1.0, 9.5, 0.5)]
                X = Y = Z = range(10, 360, 36)


            # --- Experimental ----------------------------------------------------

            elif particle == "CappedColumn01":
                print("\nStart Rendering Combined Columns...\n")
                configurations = [(4, 4, 4), (8, 8, 8), (12, 12, 12)]
                X = Y = Z = range(10, 360, 36)

            elif particle == "Plate01":
                print("\nStart Rendering Plates...\n")
                configurations = [(i, i, 1) for i in np.arange(10, 30, 4)]
                X = range(50, 140, 10)
                Y = range(0, 360, 36)
                Z = range(-30, 31, 15)

            elif particle == "Dendrite01":
                print("\nStart Rendering Snowflakes...\n")
                configurations = [(i, i, 1) for i in np.arange(10, 26, 2)]
                X = range(50, 140, 10)
                Y = range(0, 360, 36)
                Z = range(-30, 31, 15)

            # Start rendering
            for scale in configurations:
                scale_and_rotate_object(obj, scale, volume, area, X, Y, Z, directory, True)
                reset_object(obj)

    print("Rendering finished!")
