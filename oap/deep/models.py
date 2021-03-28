"""
Various models and functions for classification of optical array probe data.
"""

from tensorflow.keras.models import Model
from tensorflow.keras import backend as k, layers
from oap.__conf__ import SLICE_SIZE


def f1(y_true, y_pred):
    """
    Implementation of the F1 Score (https://en.wikipedia.org/wiki/F1_score)
    """

    def recall(y_t, y_p):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = k.sum(k.round(k.clip(y_t * y_p, 0, 1)))
        possible_positives = k.sum(k.round(k.clip(y_t, 0, 1)))
        # Recall:
        return true_positives / (possible_positives + k.epsilon())

    def precision(y_t, y_p):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = k.sum(k.round(k.clip(y_t * y_p, 0, 1)))
        predicted_positives = k.sum(k.round(k.clip(y_p, 0, 1)))
        # Precision:
        return true_positives / (predicted_positives + k.epsilon())

    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall) / (precision + recall + k.epsilon()))


def build_srnn_v1(filters=32, kernel_size=3, stacks=3, y_dim=SLICE_SIZE, x_dim=SLICE_SIZE, f1_score=False):
    """
    Simple Residual Neural Network with a variable number of residual blocks.

    Version 1.0: This model was used for the "Automatic shape detection of ice crystals"-paper.
    """

    input_tensor = layers.Input(shape=(y_dim, x_dim, 1))

    net = layers.Conv2D(filters=filters, kernel_size=kernel_size,
                        padding='same', input_shape=(y_dim, x_dim, 1))(input_tensor)
    net = layers.BatchNormalization()(net)
    net = layers.Activation('relu')(net)
    net = layers.MaxPooling2D(2, strides=2)(net)

    # Residual Layers:
    for _ in range(stacks):
        shortcut = net
        net = layers.Conv2D(filters=filters, kernel_size=kernel_size, padding='same')(net)
        net = layers.BatchNormalization()(net)
        net = layers.Activation('relu')(net)
        net = layers.add([net, shortcut])
        net = layers.MaxPooling2D(2, strides=2)(net)

    net = layers.Conv2D(filters=filters, kernel_size=kernel_size, activation='relu', padding='same')(net)
    net = layers.GlobalAveragePooling2D()(net)

    # Fully-connected Layer:
    net = layers.Dense(filters // 2, activation='relu')(net)
    output_tensor = layers.Dense(1, activation='sigmoid')(net)

    model = Model(input_tensor, output_tensor)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[f1, 'acc'] if f1_score else ['acc'])
    model.summary()

    return model


def build_srnn_v2(filters=32, kernel_size=3, stacks=3, y_dim=SLICE_SIZE, x_dim=SLICE_SIZE, f1_score=False):
    """
    Simple Residual Neural Network with a variable number of residual blocks.

    Version 2.0: The penultimate fully connected layer was removed in order to prevent too fast overfitting.
    """

    input_tensor = layers.Input(shape=(y_dim, x_dim, 1))

    net = layers.Conv2D(filters=filters, kernel_size=kernel_size,
                        padding='same', input_shape=(y_dim, x_dim, 1))(input_tensor)
    net = layers.BatchNormalization()(net)
    net = layers.Activation('relu')(net)
    net = layers.MaxPooling2D(2, strides=2)(net)

    # Residual Layers:
    for _ in range(stacks):
        shortcut = net
        net = layers.Conv2D(filters=filters, kernel_size=kernel_size, padding='same')(net)
        net = layers.BatchNormalization()(net)
        net = layers.Activation('relu')(net)
        net = layers.add([net, shortcut])
        net = layers.MaxPooling2D(2, strides=2)(net)

    net = layers.Conv2D(filters=filters, kernel_size=kernel_size, activation='relu', padding='same')(net)
    net = layers.GlobalAveragePooling2D()(net)

    # Fully-connected Layer:
    output_tensor = layers.Dense(1, activation='sigmoid')(net)

    model = Model(input_tensor, output_tensor)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[f1, 'acc'] if f1_score else ['acc'])
    model.summary()

    return model
