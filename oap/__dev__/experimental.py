"""
Experimental Functions - In Construction !!!

Author:         Lucas Tim Grulich
Created:        October 2017
Last Update:    02. August 2019
"""

from oap.__conf__ import MARKER, MONOSCALE_SHADOWLEVEL, SLICE_SIZE
from oap.utils import barycenter

import numpy as np

from copy import copy

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

from math import acos, atan, atan2, cos, degrees, radians, sin, sqrt
from scipy.cluster.hierarchy import linkage, fcluster


def vanish_poisson(array):
    vanish_color(array, color=MARKER['poisson'])


def vanish_color(array, color):
    array[array == color] = 0


def __manhattan_dist(v0, v1):
    return abs(v1[0] - v0[0]) + abs(v1[1] - v0[1])


def __euclidean_dist(v0, v1):
    return sqrt(sum(pow(x - y, 2) for x, y in zip(v0, v1)))


def __vector_length(vec):
    return sqrt(vec[0] * vec[0] + vec[1] * vec[1])


def __normalize(vec):
    length = __vector_length(vec)
    return [vec[0] / length, vec[1] / length] if length > 0 else [0, 0]


def __degree(vec0, vec1):
    vec0 = __normalize(vec0)
    vec1 = __normalize(vec1)

    x = vec0[0] * vec1[0] + vec0[1] * vec1[1]
    if -1 <= x <= 1:
        return degrees(acos(x))
    return degrees(acos(round(x)))


def __vector_shift_in_radians(vec0, vec1):
    vec0 = __normalize(vec0)
    vec1 = __normalize(vec1)
    return atan2(vec0[1], vec0[0]) - atan2(vec1[1], vec1[0])


# ToDo: recursive depth
def __floodfill(array, x, y, marker, colors, diagonal=False, horizontal=True, slice_size=SLICE_SIZE):
    """
    Recursive FloodFill Alogrithm for optical arrays
    as 1 dimensional list or numpy array.

    :param array:       optical array (particle image)
    :type array:        numpy array (1 dimensional) or list or string

    :param x:           x-index
    :type x:            integer

    :param y:           y-index
    :type y:            integer

    :param marker:      color-value of the filling
    :type marker:       integer

    :param colors:      list of colors, which shall be colored
    :type colors:       list of integers

    --- optional params ---
    :param diagonal:    filling in diagonal direction (default == False)
    :type diagonal:     boolean

    :param horizontal:  filling in horizontal direction (default == True)
    :type horizontal:   boolean

    :param slice_size:   width of the optical array (number of diodes)
    :type slice_size:    integer

    :return:             this (recursive)
    """
    if 0 <= x < slice_size and 0 <= y < (len(array) / slice_size):

        if array[y*slice_size+x] not in colors:
            return

        if array[y*slice_size+x] != marker:
            array[y*slice_size+x] = marker
            try:
                if horizontal:
                    __floodfill(array, x + 1, y, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x - 1, y, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x, y + 1, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x, y - 1, marker, colors, diagonal, horizontal, slice_size)
                if diagonal:
                    __floodfill(array, x + 1, y + 1, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x + 1, y - 1, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x - 1, y + 1, marker, colors, diagonal, horizontal, slice_size)
                    __floodfill(array, x - 1, y - 1, marker, colors, diagonal, horizontal, slice_size)
            except:
                return
    return


def principal_axes(array,
                   noise=False,
                   mindegree=175.0,
                   metric="cityblock",
                   method="average",
                   maxdistance=6.2,
                   merge=17.8,
                   mergingmethod="average",
                   dimensionfactor=1.3,
                   plot=(0, 0, 0),
                   slicesize=SLICE_SIZE):
    """
    This method finds parts of the particle image, which stick out (so called vertices).
    For example the individual bullets of a combined bullet or the arms of a snowflake.

    Returns the number of vertices and the number of vectors, which point from
    the barycenter to the individual vertices, which are nearly in one line
    (the threshold is the minimum degree).

    Returns also the variance of the vector lengths and the length and width of the stick out parts.

    Perfect ice crystals should have 6 vertices, 3 straight lines and a small variance.
    Needles or Columns should have 2 vertices, 1 straight line and a small variance.
    Combined bullets should have at least 3 vertices.
    Thats just an example! These values differ for different clustering methods, maximum distances,
    degrees and the method of merging vectors.

    Created: March / April 2018 in St. Louis, MO
    """

    # Copy of array.
    array_copy = copy(array)

    x_bary, y_bary = barycenter(array_copy, coordinates=False, slice_size=slicesize)
    x_bary_coord, y_bary_coord = barycenter(array_copy, slice_size=slicesize)

    if array_copy[y_bary_coord * slicesize + x_bary_coord] == 0 \
            or array_copy[y_bary_coord * slicesize + x_bary_coord] == MARKER['poisson']:
        return False

    if not noise:
        __floodfill(array_copy, x_bary_coord, y_bary_coord, MARKER['floodfill'],
                    colors=[1, 2, 3, MARKER['poisson'], MARKER['floodfill']])

        # Delete noisy components of the optical array.
        for i in range(len(array_copy)):
            if array_copy[i] and array_copy[i] != MARKER['floodfill']:
                array_copy[i] = 0

    slices = int(len(array_copy) / slicesize)

    sum_distance = 0.0
    number_of_pixels = 0

    # Calculate the average distance of every shadowed pixel to the
    # particle barycenter.
    for y in range(slices):
        for x in range(slicesize):
            if array_copy[y * slicesize + x]:
                sum_distance += __euclidean_dist((x_bary, y_bary), (x, y))
                number_of_pixels += 1

    avg_distance = sum_distance / number_of_pixels
    stick_out_pixels = []
    remaining_pixels = []

    # Find the pixels, which stick out of the particle core.
    inner_pixel_array = np.zeros(len(array))
    for y in range(slices):
        for x in range(slicesize):
            if array_copy[y * slicesize + x]:
                if avg_distance <= __euclidean_dist((x_bary, y_bary), (x, y)):
                    stick_out_pixels.append([x, y])
                else:
                    inner_pixel_array[y * slicesize + x] = 2
                    remaining_pixels.append([x, y])

    # Calculate a new barycenter for the inner pixel group  of the optical array.
    try:
        x_new_bary, y_new_bary = barycenter(inner_pixel_array,
                                            coordinates=False,
                                            slice_size=slicesize)
    except TypeError:
        return False

    stick_out_pixels = np.array(stick_out_pixels)
    remaining_pixels = np.array(remaining_pixels)

    # Ratio of pixels ticking out to the total number of pixels.
    # ratio = float(len(stick_out_pixels)) / (len(stick_out_pixels)+len(remaining_pixels))

    if not len(stick_out_pixels) >= 2:
        return False

    # Manhattan Clustering of the sticking out pixels.
    z = linkage(stick_out_pixels, method=method, metric=metric)
    # Clustering with maximum distance between clusters.
    clusters = fcluster(z, maxdistance, criterion='distance')

    number_of_stick_outs = max(clusters)
    largest_distances = np.zeros(number_of_stick_outs)

    for i, v in enumerate(stick_out_pixels):
        if __euclidean_dist((x_new_bary, y_new_bary), v) > largest_distances[clusters[i] - 1]:
            largest_distances[clusters[i] - 1] = __euclidean_dist((x_new_bary, y_new_bary), v)

    # Point the vectors to the barycenter of the different clusters.
    vectors = []
    cluster_barycenters = []

    plot_vectors = []

    for i in range(max(clusters)):

        pixels = np.zeros(len(array))
        for j, pxl in enumerate(stick_out_pixels):
            if i == clusters[j] - 1:
                pixels[pxl[1] * slicesize + pxl[0]] = 2

        x_vec, y_vec = barycenter(pixels, coordinates=False, slice_size=slicesize)
        vec = [x_vec - x_new_bary, y_vec - y_new_bary]

        cluster_barycenters.append([x_vec, y_vec])

        # Calculate scale to set the vector size to the largest distance.
        vec_length = __vector_length(vec)
        if vec_length:
            vec_scale = largest_distances[i] / vec_length
        else:
            vec_scale = 1.0

        # Update vector with the new scale.
        vec = [vec_scale * vec[0], vec_scale * vec[1]]
        vectors.append(vec)
        if plot:
            plot_vectors.append((x_new_bary, y_new_bary, vec[0], vec[1]))

    old_clusters = None
    # --- Agglomerative Clustering of close vectors ---
    #
    # The degree between vectors determines if they are close.
    # Vectors which degrees are smaller than the "merge" value get merged.
    # User can switch between single or average clustering of vectors.
    if merge:
        # First step: every vector is in its own cluster.
        joined_vectors = [[[v, i]] for i, v in enumerate(vectors)]

        while True:
            min_degree = 361
            join_index_1 = 0
            join_index_2 = 0

            for c_1, cluster_1 in enumerate(joined_vectors):
                for c_2, cluster_2 in enumerate(joined_vectors):
                    if c_1 == c_2 or len(cluster_1) == 0 or len(cluster_2) == 0:
                        continue

                    if mergingmethod.upper() == "AVERAGE":
                        # Average Clustering
                        avg_vec_1 = [0, 0]
                        for vec in cluster_1:
                            avg_vec_1[0] += vec[0][0]
                            avg_vec_1[1] += vec[0][1]
                        avg_vec_1[0] /= len(cluster_1)
                        avg_vec_1[1] /= len(cluster_1)

                        avg_vec_2 = [0, 0]
                        for vec in cluster_2:
                            avg_vec_2[0] += vec[0][0]
                            avg_vec_2[1] += vec[0][1]
                        avg_vec_2[0] /= len(cluster_2)
                        avg_vec_2[1] /= len(cluster_2)

                        deg = __degree(avg_vec_1, avg_vec_2)
                        if deg < min_degree:
                            min_degree = deg
                            join_index_1 = c_1
                            join_index_2 = c_2
                    elif mergingmethod.upper() == "SINGLE":
                        for vec_1 in cluster_1:
                            for vec_2 in cluster_2:
                                deg = __degree(vec_1[0], vec_2[0])
                                if deg < min_degree:
                                    min_degree = deg
                                    join_index_1 = c_1
                                    join_index_2 = c_2

            # Break if there are no more clusters to merge.
            if min_degree > merge:
                break
            # Join closest clusters.
            joined_vectors[join_index_1] += joined_vectors[join_index_2]
            joined_vectors[join_index_2] = []

        # Overwrite clusters with other information. The following function needs the vector lengths and their indices.
        # Hence the new clusters provide both informations.
        joined = []
        for j_vecs in joined_vectors:
            if len(j_vecs) == 0:
                continue
            new_cluster = []
            for v in j_vecs:
                new_cluster.append([__vector_length(v[0]), v[1]])
            joined.append(sorted(new_cluster, reverse=True))
        joined_vectors = joined

        # Find the new barycenter of the new joined vector.
        merged_barycenters = []
        for j_vecs in joined_vectors:
            merged_center = [0, 0]

            for v in j_vecs:
                merged_center[0] += cluster_barycenters[v[1]][0]
                merged_center[1] += cluster_barycenters[v[1]][1]
            merged_center[0] /= len(j_vecs)
            merged_center[1] /= len(j_vecs)
            merged_barycenters.append(merged_center)

        old_clusters = copy(clusters)
        for i, j_vecs in enumerate(joined_vectors):
            # Join Clusters -> Clusters get the value of the cluster with the longest vector.
            for j in range(len(clusters)):
                if clusters[j] - 1 in [v[1] for v in j_vecs]:
                    clusters[j] = j_vecs[0][1] + 1

            # Calcluate the new scale and the new Vector direction.
            vec_scale = largest_distances[j_vecs[0][1]] / __vector_length(
                [merged_barycenters[i][0] - x_new_bary, merged_barycenters[i][1] - y_new_bary])
            vectors[j_vecs[0][1]] = [vec_scale * (merged_barycenters[i][0] - x_new_bary),
                                     vec_scale * (merged_barycenters[i][1] - y_new_bary)]
            if plot:
                plot_vectors[j_vecs[0][1]] = (x_new_bary, y_new_bary,
                                              vectors[j_vecs[0][1]][0], vectors[j_vecs[0][1]][1])

            # Set merged vectors to None.
            for j in range(1, len(j_vecs)):
                vectors[j_vecs[j][1]] = None
                if plot:
                    plot_vectors[j_vecs[j][1]] = None

    # --- Dimension Calculation ---
    dimensions = []
    if dimensionfactor:
        for i in range(max(clusters)):

            # Some clusters might be empty, because of the merging process.
            empty = True
            pixels = np.zeros(len(array))
            for j, pxl in enumerate(stick_out_pixels):
                if i == clusters[j] - 1:
                    pixels[pxl[1] * slicesize + pxl[0]] = 2
                    empty = False
            if empty:
                continue

            # Calculate the width of the cluster in dependence of the vector rotation.
            theta = __vector_shift_in_radians([0, 1], vectors[i])
            pixels_x = []
            pixels_y = []
            for y in range(int(len(pixels) / slicesize)):
                for x in range(slicesize):

                    if pixels[y * slicesize + x]:
                        px = x * cos(theta) - y * sin(theta)
                        # Rotation of y is not necessary, but is needed for debugging.
                        py = x * sin(theta) + y * cos(theta)
                        pixels_x.append(px)
                        pixels_y.append(py)

            # Calculate the variance in the x direction
            sum_x = 0
            sum_xx = 0
            for j in range(len(pixels_x)):
                sum_x += pixels_x[j]
                sum_xx += pixels_x[j] * pixels_x[j]

            x_bary_rotation = sum_x / len(pixels_x)
            var_x = sum_xx / len(pixels_x) - x_bary_rotation * x_bary_rotation
            discriminant = sqrt(4 * var_x * var_x)
            width = dimensionfactor * 2 * sqrt(((var_x + var_x) + discriminant) / 2.0)

            dimensions.append([__vector_length(vectors[i]), width])

    if merge:
        # Remove objects in vector lists, which are equal to None.
        # Objects which are None got deleted in the vector and cluster merging process above.
        # The deletion must be down here, because it changes the indices of the vectors.
        # The correct vector indices are needed for the dimension calculations
        vectors = [x for x in vectors if x is not None]
        if plot:
            plot_vectors = [x for x in plot_vectors if x is not None]

    # Calculate the mean and the variance of vector lengths.
    mean = sum([__vector_length(vec) for vec in vectors]) / float(len(vectors))
    variance = sum([pow(__vector_length(vec) - mean, 2) for vec in vectors]) \
               / float(len(vectors))

    # Find the number of vectors which are nearly in a straight line.
    # In other words: Vectors which are nearly parallel to each other.
    angles = []
    nearly_straight_angles = 0
    for i, vec0 in enumerate(vectors):
        for j, vec1 in enumerate(vectors):
            if i == j:
                break
            angle = round(__degree(vec0, vec1), 2)
            if angle >= mindegree:
                nearly_straight_angles += 1
                angles.append(angle)

    if plot:

        if plot[0]:
            if plot[0] == 1:
                plt.scatter(stick_out_pixels[:, 0], stick_out_pixels[:, 1], c=clusters, cmap="jet")
            elif plot[0] == 2:
                plt.scatter(stick_out_pixels[:, 0], stick_out_pixels[:, 1], c=old_clusters, cmap="jet")
            else:
                plt.scatter(stick_out_pixels[:, 0], stick_out_pixels[:, 1], c="gray")
            plt.scatter(remaining_pixels[:, 0], remaining_pixels[:, 1], c="gray")

        ax = plt.gca()
        ax.invert_yaxis()
        ax.set_aspect(1)

        if plot[1] == 1:
            a, b, c, d = zip(*plot_vectors)
            plt.quiver(a, b, c, d, angles='xy', scale_units='xy', scale=1, width=0.01)

        elif plot[1] == 2 and dimensionfactor:

            for i, v in enumerate(vectors):
                theta = __vector_shift_in_radians([0, 1], v)
                trans = Affine2D().rotate_around(x_new_bary, y_new_bary, -theta)

                hexagon_1 = Rectangle((x_new_bary, y_new_bary),
                                      dimensions[i][1] / 2.0, dimensions[i][0],
                                      fill=True,
                                      edgecolor="black",
                                      alpha=0.3,
                                      linewidth=1)
                hexagon_2 = Rectangle((x_new_bary, y_new_bary),
                                      -dimensions[i][1] / 2.0, dimensions[i][0],
                                      fill=True,
                                      edgecolor="black",
                                      alpha=0.3,
                                      linewidth=1)

                hexagon_1.set_transform(trans + ax.transData)
                hexagon_2.set_transform(trans + ax.transData)
                ax.add_patch(hexagon_1)
                ax.add_patch(hexagon_2)

        if plot[2]:
            cluster_barycenters = np.array(cluster_barycenters)
            plt.scatter(cluster_barycenters[:, 0], cluster_barycenters[:, 1], c="black")

            plt.scatter(x_bary, y_bary, c="red")
            plt.scatter(x_new_bary, y_new_bary, c="black")

        plt.show()

    return number_of_stick_outs, \
           nearly_straight_angles, \
           angles, \
           round(variance, 3), \
           dimensions


def __mse(array_a, array_b):
    """
    Mean Squared Error: The two arrays must have the same dimension.
    """
    error = np.sum((array_a.astype("float") - array_b.astype("float")) ** 2)
    # Divide by the number of imagepixels
    error /= float(len(array_a))
    # The lower the error, the more similar the two images are.
    return error


def __polygon_intersection(verts, x, y):
    """
    Computes the intersection with a polygon.

    Algorithm from:
    W. Randolph Franklin (WRF)
    https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html#The Method
    """
    intersection = False
    for i in range(len(verts)):
        j = (i + len(verts) - 1) % len(verts)
        if (verts[i][1] > y) != (verts[j][1] > y) \
                and x < (verts[j][0] - verts[i][0]) * (y - verts[i][1]) / (verts[j][1] - verts[i][1]) + verts[i][0]:
            intersection = not intersection
    return intersection


def __polygon_rotation(verts, alpha, point):
    """
    Rotates an Object around a specific point.

    Parameter: List of 2d vertices represented as tuple (x,y)
               The angle in radians
               A 2d point (x,y) as Tuple, List or Array

    Returns:   The rotated object
    """
    polygon = []
    cos_alpha = cos(alpha)
    sin_alpha = sin(alpha)
    for v in verts:
        x = v[0] * cos_alpha - sin_alpha * v[1] + point[0]
        y = v[0] * sin_alpha + cos_alpha * v[1] + point[1]
        polygon.append((x, y))
    return polygon


def principal_components(array, dimensionfactor=1.0, plot=None, slicesize=SLICE_SIZE):
    """
    Calculates the Principal Components of an Optical Array.
    """
    sum_x = 0.0
    sum_y = 0.0
    sum_xx = 0.0
    sum_yy = 0.0
    sum_xy = 0.0
    number_pix = 0.0

    for y in range(int(len(array) / slicesize)):
        for x in range(slicesize):
            if array[y * slicesize + x]:
                sum_x += x
                sum_y += y
                sum_xx += x * x
                sum_yy += y * y
                sum_xy += x * y
                number_pix += 1

    if number_pix == 0:
        return

    x_bary = sum_x / number_pix
    y_bary = sum_y / number_pix

    # Calculating the variance and the covariance.
    var_x = sum_xx / number_pix - x_bary * x_bary
    var_y = sum_yy / number_pix - y_bary * y_bary
    cov_xy = sum_xy / number_pix - x_bary * y_bary

    discriminant = (var_x - var_y) * (var_x - var_y) + 4 * cov_xy * cov_xy
    sqrt_discr = sqrt(discriminant)

    lambda_plus = ((var_x + var_y) + sqrt_discr) / 2.0
    lambda_minus = ((var_x + var_y) - sqrt_discr) / 2.0

    # --- Eigenvectors ---
    x_plus = var_x + cov_xy - lambda_minus
    y_plus = var_y + cov_xy - lambda_minus
    x_minus = var_x + cov_xy - lambda_plus
    y_minus = var_y + cov_xy - lambda_plus

    # Normalizing the vectors.
    denom_plus = sqrt(x_plus * x_plus + y_plus * y_plus)
    denom_minus = sqrt(x_minus * x_minus + y_minus * y_minus)

    # Computing the normalized vector, which is parallel to the
    # longest axis of a particle image.
    if denom_plus:
        x_parallel = x_plus / denom_plus
        y_parallel = y_plus / denom_plus
    else:
        x_parallel = x_plus
        y_parallel = y_plus
    # Computing the normalized vector, which is corresponding the
    # Normal of a particle image.
    if denom_minus:
        x_normal = x_minus / denom_minus
        y_normal = y_minus / denom_minus
    else:
        x_normal = x_minus
        y_normal = y_minus

    if lambda_plus < 0:
        lambda_plus = 0
    if lambda_minus < 0:
        lambda_minus = 0
    major_axis = dimensionfactor * 2 * sqrt(lambda_plus)
    minor_axis = dimensionfactor * 2 * sqrt(lambda_minus)

    # Computing the rotation of the principal components.
    if x_parallel:
        alpha = atan(y_parallel / x_parallel)
    else:
        alpha = radians(90.0)

    # --- Polygon ------------------------------------------------------------------------------------------------------
    """
    scale_1 = 0.75
    scale_2 = 1.0
    scale_3 = 1.0
    scale_4 = 0.5

    vert_1 = (-major_axis * scale_1,  minor_axis * scale_2)
    vert_2 = ( major_axis * scale_1,  minor_axis * scale_2)
    vert_3 = ( major_axis * scale_1, -minor_axis * scale_2)
    vert_4 = (-major_axis * scale_1, -minor_axis * scale_2)
    vert_5 = (-major_axis * scale_3,  minor_axis * scale_4)
    vert_6 = ( major_axis * scale_3,  minor_axis * scale_4)
    vert_7 = ( major_axis * scale_3, -minor_axis * scale_4)
    vert_8 = (-major_axis * scale_3, -minor_axis * scale_4)

    polygon = [vert_5, vert_1, vert_2, vert_6,
              vert_7, vert_3, vert_4, vert_8]
    polygon = __polygon_rotation(object, alpha, (x_bary, y_bary))
    """
    vert_1 = (-major_axis, minor_axis)
    vert_2 = (major_axis, minor_axis)
    vert_3 = (major_axis, -minor_axis)
    vert_4 = (-major_axis, -minor_axis)

    polygon = [vert_1, vert_2, vert_3, vert_4]
    polygon = __polygon_rotation(polygon, alpha, (x_bary, y_bary))

    cos_alpha = cos(alpha)
    sin_alpha = sin(alpha)

    # ToDo: perhaps a return would be better here
    if minor_axis == 0:
        minor_axis = 1e-8
    if major_axis == 0:
        major_axis = 1e-8

    b = minor_axis * minor_axis
    a = major_axis * major_axis

    polygon_array = np.zeros(len(array), "int")
    ellipse_array = np.zeros(len(array), "int")
    one_color_array = np.zeros(len(array), "int")

    polygon_hits = 0
    ellipse_hits = 0
    polygon_misses = 0
    ellipse_misses = 0

    points = [[], [], []]

    for y in range(int(len(array) / slicesize)):
        for x in range(slicesize):

            denom_x = cos_alpha * (x - x_bary) + sin_alpha * (y - y_bary)
            denom_y = sin_alpha * (x - x_bary) - cos_alpha * (y - y_bary)
            intersect_ellipse = ((denom_x * denom_x) / a) + ((denom_y * denom_y) / b) <= 1

            intersect_polygon = __polygon_intersection(polygon, x, y)

            if plot:
                if intersect_ellipse and array[y * slicesize + x]:
                    points[0].append([x, y])
                elif intersect_polygon and array[y * slicesize + x]:
                    points[1].append([x, y])
                elif array[y * slicesize + x]:
                    points[2].append([x, y])

            if intersect_ellipse and array[y * slicesize + x]:
                ellipse_hits += 1
            elif array[y * slicesize + x]:
                ellipse_misses += 1
            elif intersect_ellipse and array[y * slicesize + x] == 0:
                ellipse_misses += 1

            if intersect_polygon and array[y * slicesize + x]:
                polygon_hits += 1
            elif array[y * slicesize + x]:
                polygon_misses += 1

            if intersect_ellipse:
                ellipse_array[y * slicesize + x] = MONOSCALE_SHADOWLEVEL
            if intersect_polygon:
                polygon_array[y * slicesize + x] = MONOSCALE_SHADOWLEVEL
            if array[y * slicesize + x]:
                one_color_array[y * slicesize + x] = MONOSCALE_SHADOWLEVEL

    # Calculate the mean and the variance of vector lengths.
    # mean = (major_axis + minor_axis) / 2.0
    # variance = ((major_axis - mean) * (major_axis - mean) + (minor_axis - mean) * (minor_axis - mean)) / 2.0
    hit_ratio = ellipse_hits / float(ellipse_misses + ellipse_hits)
    alpha_value = degrees(alpha)
    axis_ratio = major_axis / minor_axis

    if plot is not None:

        points[0] = np.array(points[0])
        points[1] = np.array(points[1])
        points[2] = np.array(points[2])

        if plot[0] == 1 and len(points[0]):
            plt.scatter(points[0][:, 0], points[0][:, 1], c="#04466c")
        if plot[1] == 1 and len(points[1]):
            plt.scatter(points[1][:, 0], points[1][:, 1], c="#ff0000", alpha=0.75, marker="s")
        if plot[2] == 1 and len(points[2]):
            plt.scatter(points[2][:, 0], points[2][:, 1], c="#cc3f3f", alpha=0.75, marker="s")
        if plot[3] == 1 and len(points[2]) and False:
            plt.scatter(points[2][:, 0], points[2][:, 1], c="#ff0000", alpha=0.75, marker="s")

        array = np.array(array)
        vanish_poisson(array)
        image = np.reshape(array, (int(len(array) / 64), 64))

        plt.imshow(image, cmap="Greys_r")

        if y_normal < 0:
            vectors = [(x_bary, y_bary, x_parallel * major_axis, y_parallel * major_axis),
                       (x_bary, y_bary, -x_parallel * major_axis, -y_parallel * major_axis),
                       (x_bary, y_bary, x_normal * minor_axis, y_normal * minor_axis),
                       (x_bary, y_bary, -x_normal * minor_axis, -y_normal * minor_axis)]
            txt_center_x = x_bary + (x_normal * minor_axis)
            txt_center_y = y_bary + (y_normal * minor_axis)
        else:
            vectors = [(x_bary, y_bary, -x_parallel * major_axis, -y_parallel * major_axis),
                       (x_bary, y_bary, x_parallel * major_axis, y_parallel * major_axis),
                       (x_bary, y_bary, -x_normal * minor_axis, -y_normal * minor_axis),
                       (x_bary, y_bary, x_normal * minor_axis, y_normal * minor_axis)]
            txt_center_x = x_bary + (-x_normal * minor_axis)
            txt_center_y = y_bary + (-y_normal * minor_axis)

        if alpha < 0:
            horizontal = "right"
        else:
            horizontal = "left"

        # Plot Principal Components.
        x, y, u, v = zip(*vectors)
        plt.quiver(x_bary, y_bary, 0, -y_bary-0.5, angles='xy', scale_units='xy', scale=1, width=0.0075, headlength=0, headwidth=1,
                   color="grey")
        plt.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, width=0.01, headlength=0, headwidth=1,
                   color=["#1f77b4", "#1f77b4", "#ff7f0e", "#ff7f0e"], label="Major Axis")
        plt.scatter(x_bary, y_bary, marker="o", color="#1f77b4", label="Barycenter")

        plt.text(x=txt_center_x, y=txt_center_y-0.5, s=f"{round(alpha_value, 3)}°", verticalalignment="bottom", horizontalalignment=horizontal, color="#ff7f0e")
        #plt.text(x=0, y=-10, s=f"Hit Ratio: {round(hit_ratio, 3)}\nAspect Ratio: {round(axis_ratio, 3)}",
        #         color="white", verticalalignment="bottom")

        if plot[3] == 1:
            # Plot Polygon.
            polygon_verts = len(polygon)
            for i in range(polygon_verts):
                if i == 0:
                    plt.plot((polygon[i % polygon_verts][0], polygon[(i + 1) % polygon_verts][0]),
                             (polygon[i % polygon_verts][1], polygon[(i + 1) % polygon_verts][1]),
                             linewidth=1.2, c="#d62728", label="Rectangle")
                else:
                    plt.plot((polygon[i % polygon_verts][0], polygon[(i + 1) % polygon_verts][0]),
                             (polygon[i % polygon_verts][1], polygon[(i + 1) % polygon_verts][1]),
                             linewidth=1.2, c="#d62728", )

        # Plot Ellipse.
        array_length = 1000
        theta = np.linspace(0, 2 * np.pi, array_length)

        # Transform cartesian coordinates to polar coordinates.
        x = major_axis * np.cos(theta)
        y = minor_axis * np.sin(theta)

        plt.plot((x * cos(alpha) - sin(alpha) * y) + x_bary,
                 (x * sin(alpha) + cos(alpha) * y) + y_bary,
                 linewidth=1.8, c="#2ca02c", label="Ellipse")

        from matplotlib.ticker import MultipleLocator
        ax = plt.gca()
        ax.set_facecolor("black")
        ax.set_aspect(1)

        #plt.xlabel("Diode Array")
        #plt.ylabel("Flight Direction")
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        #ax.xaxis.set_major_locator(MultipleLocator(5))
        #ax.yaxis.set_major_locator(MultipleLocator(5))

        plt.xlim(plot[4])
        #ax.set_yticks(np.arange(-.5, int(len(array)/slicesize), 5))
        #ax.set_xticklabels(np.arange(0, 65+0.5, 5, dtype=int))
        #ax.set_yticklabels(np.arange(0, int(len(array)/slicesize)+0.5, 5, dtype=int))

        #plt.axes().yaxis.set_minor_locator(MultipleLocator(1))

        #plt.grid(which='minor', color='red', linestyle='-', linewidth=0.5, alpha=0.5)
        # plt.legend()
        # plt.savefig(plot[4])

    return hit_ratio, \
           __mse(one_color_array, ellipse_array), \
           polygon_hits / float(polygon_misses + polygon_hits) * 100, \
           __mse(one_color_array, polygon_array), \
           alpha_value, \
           axis_ratio, \
           (2 * major_axis, 2 * minor_axis)


def connected_components(array, slicesize=SLICE_SIZE):
    """
    Returns the number of Connected Components of an optical array
    as 1 dimensional list or numpy array.

    CAUTION: If the particle image is to big and the recursion depth of Python is
             to low, number_of_components will incremented more than once, since the
             the recursion will be interrupted and will be later continued with a
             new marker.
    """
    # Start with a high number as marker.
    marker = 100
    used_markers = []
    number_of_components = 0

    # Create copy of array. Otherwise the original
    # optical array will be colored.
    array_copy = copy(array)

    for y in range(int(len(array_copy) / slicesize)):
        for x in range(slicesize):
            if array_copy[y*slicesize+x] != 0 and not int(array_copy[y*slicesize+x]) in used_markers:
                # Color the component and then change the marker.
                __floodfill(array_copy, x, y, marker, colors=[1, 2, 3, MARKER['poisson'], marker], diagonal=True)
                used_markers.append(marker)
                number_of_components += 1
                marker += 1

    return number_of_components


# ToDo: recursive depth
def __poisson(array, x, y, counter=0):
    if counter > 64*30: # ToDo: Extremely bad solution -> think of an other algorithm for poisson detection!
        return
    if 0 <= x < 64 and 0 <= y < (len(array) / 64):
        if array[y*64+x] != 0:
            return
        if array[y*64+x] != 7:
            array[y*64+x] = 7
            try:
                __poisson(array, x + 1, y, counter+1)
                __poisson(array, x - 1, y, counter+1)
                __poisson(array, x, y + 1, counter+1)
                __poisson(array, x, y - 1, counter+1)
            except:
                return
        return
    return


# ToDo: check_y doesn't work on images with frames (not clipped)
def poisson_spot(array, sizing=False, check_y=False, slice_size=SLICE_SIZE):
    """
    If the particle has a Poisson Spot, the function fills the spot with a marker.
    Returns also the Poisson diameter, if sizing is True.

    If poisson spot is not closed in x-direction it is not possible to measure the
    spot size. Hence, the marker will be removed. If checkAlsoY is true the poisson spot
    must be closed in y direction too.

    :param array:       optical array (particle image)
    :type array:        numpy array (1 dimensional) or list or string

    --- optional params ---
    :param sizing:      if True and there is a spot -> returns spot size in pixels
    :type sizing:       boolean

    :param check_y:     if True -> checks the first and last slice, if spot is closed
    :type check_y :     boolean

    :param slice_size:  width of the optical array (number of diodes)
    :type slice_size:   integer

    :return:            True or spot size in pixels (if spot is closed) or False
    """
    y_bary, x_bary = barycenter(array, coordinates=True, slice_size=slice_size)
    __poisson(array, x_bary, y_bary)

    # Check if the Poisson Spot is closed. If the edges of a particle images are
    # colored with the Poisson Spot marker, the Spot cannot be closed.
    spot_is_closed = True

    for y in range(int(len(array) / slice_size)):
        if array[y * slice_size] == MARKER['poisson'] or array[y * slice_size + (slice_size - 1)] == MARKER['poisson']:
            spot_is_closed = False

    if spot_is_closed and check_y:
        for x in range(slice_size):
            if array[x] == MARKER['poisson']\
                    or array[int(((len(array) / slice_size) - 1) * slice_size + x)] == MARKER['poisson']:
                spot_is_closed = False

    # If the spot is not closed, the Poisson Spot marker gets deleted.
    if not spot_is_closed:
        for y in range(int(len(array) / slice_size)):
            for x in range(slice_size):
                if array[y * slice_size + x] == MARKER['poisson']:
                    array[y * slice_size + x] = 0

    # If sizing is True, the function returns the Poisson Spot diameter.
    if sizing and spot_is_closed:
        min_poisson_index = slice_size - 1
        max_poisson_index = 0
        for y in range(int(len(array) / slice_size)):
            for x in range(slice_size):
                if array[y * slice_size + x] == MARKER['poisson'] and x > max_poisson_index:
                    max_poisson_index = x
                if array[y * slice_size + x] == MARKER['poisson'] and x < min_poisson_index:
                    min_poisson_index = x
        poisson_diameter = max_poisson_index - min_poisson_index + 1
        poisson_diameter = poisson_diameter if poisson_diameter > 0 else 0
        return poisson_diameter
    else:
        if spot_is_closed:
            return True
        else:
            return False
