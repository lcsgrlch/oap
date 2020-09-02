"""
Various data import functions for training and validation of neural networks.
"""

import numpy as np
import random as rnd

from oap.__conf__ import OAP_FILE_EXTENSION, SLICE_SIZE
from oap.lib import normalize
from oap.utils import (
    barycenter,
    features,
    adjust_y,
    center_particle,
    flip_x,
    flip_y,
    monochromatic,
    move_to_x,
    move_to_y
)
from oap.utils.files import filepaths, read_oap_file


def generator(directory, positive, batch_size=1, y_dim=SLICE_SIZE, balance=False, shuffle=False,
              monochrome=False, center=False, move=True, flip=True, exclude=None, include=None,
              file_extension=OAP_FILE_EXTENSION, slice_size=SLICE_SIZE):
    """
    oap-file generator for training with neural networks.
    Especially developed to train / validate a model with the Keras library.
    (see Keras - Class: tf.keras.Model | Method: fit_generator).

    :param directory:       path to directory
    :type directory:        string

    :param positive:        list of particle types for positive labeling
    :type positive:         list

    --- optional params ---
    :param batch_size:      size of the data batch
    :type batch_size:       int

    :param y_dim:           height of the particle image / optical-array
    :type y_dim:            int

    :param balance:         balances the positive data with the same number of negative data
    :type balance:          boolean

    :param shuffle:         shuffles the data before every epoch
    :type shuffle:          boolean

    :param monochrome:      converts the optical array to monochromatic shadow levels (just ones and zeros)
    :type monochrome:       boolean

    :param center:          centers the particle in the image frame (only in x-axis)
    :type center:           boolean

    :param move:            randomly moves the particle within the image frame
                            Warning: only works, if center == False
    :type move:             boolean

    :param flip:            randomly flips the array in x and / or y direction
    :type flip:             boolean

    :param exclude:         list of folders which should be excluded
    :type exclude:          list of strings

    :param include:         list of folders to include - ignores all other folders
    :type include:          list of strings

    :param file_extension:  file type
    :type file_extension:   string

    :param slice_size:      width of the optical array (number of diodes)
    :type slice_size:       integer

    :return:                image-tensor (shape: (batch_size, y_dim, x_dim, 1),
                            label-tensor (len == batch_size)
    """
    positive_files = []
    negative_files = []

    if balance:
        positive_files = filepaths(directory, exclude=exclude, include=include,
                                   file_extension=file_extension, p_types=positive)
        negative_files = [f for f in filepaths(directory, exclude=exclude, include=include,
                                               file_extension=file_extension) if f not in positive_files]
        files = rnd.sample(negative_files, len(positive_files)) + positive_files
    else:
        files = filepaths(directory, exclude=exclude, include=include, file_extension=file_extension)

    number_of_batches = len(files) // batch_size
    rnd.shuffle(files)
    batch_iterator = 0

    while True:

        if batch_iterator >= number_of_batches:
            batch_iterator = 0

            if balance:
                # Sample new negative files
                files = rnd.sample(negative_files, len(positive_files)) + positive_files
            if shuffle:
                rnd.shuffle(files)

        x = []  # Data
        y = []  # Labels

        for i in range(batch_size):
            array, header = read_oap_file(filename=files[batch_iterator*batch_size+i],
                                          as_type="ARRAY", slice_size=slice_size)
            if monochrome:
                array = monochromatic(array, slice_size=slice_size)

            if flip:
                if bool(rnd.getrandbits(1)):
                    array = flip_y(array, slice_size=slice_size)
                if bool(rnd.getrandbits(1)):
                    array = flip_x(array, slice_size=slice_size)

            # Unify the height of the optical array.
            array = adjust_y(array, new_y=y_dim, slice_size=slice_size)

            if center:
                center_particle(array, slice_size=slice_size)
            elif move:
                feat = features(array, slice_size=slice_size)
                x_bary, y_bary = barycenter(array, coordinates=True)

                # Random uniform between top border and bottom border
                new_y = int(rnd.uniform(y_bary, y_dim - y_bary))
                array = move_to_y(array, new_y=new_y, slice_size=slice_size)

                # Random uniform between left border and right border
                new_x = int(rnd.uniform(x_bary-feat['min_index'], slice_size-(feat['max_index']-x_bary)))
                array = move_to_x(array, new_x=new_x, slice_size=slice_size)

            # Normalize!
            array = normalize(array, value=1.0 if monochrome else 3.0)

            label = 1.0 if header in positive else 0.0

            # Reshape to Height x Width x Number of Channels
            x.append(array.reshape(y_dim, slice_size, 1))
            y.append(label)

        batch_iterator += 1
        yield np.array(x), np.array(y)
