__author__ = "Lucas Grulich (grulich@uni-mainz.de)"
__version__ = "0.0.14"

# --- Globals ----------------------------------------------------------------------------------------------------------
MONOSCALE_SHADOWLEVEL = 1
OAP_FILE_EXTENSION = ".oap"
DEFAULT_TYPE = "ARRAY2D"
SLICE_SIZE = 64

# --- Markers ------------------------------------------------
MARKER = {
    'poisson':    7,     # Value of the poisson spot
    'flood_fill': 8,     # Value of the flood fill
}

# --- Colors -------------------------------------------------
COLOR = {
    0: 0,                   # Shadow level 0 -> background color of images.
    1: 100,                 # Shadow level 1 -> usually between 25% and 33%
    2: 200,                 # Shadow level 2 -> light intensity of 50 %
    3: 255,                 # Shadow level 3 -> usually between 66% and 75%
    MARKER['poisson']: 50,  # Poisson spot color
}

# --- Particle Types -----------------------------------------
UNDEFINED = b'u'    # Not yet classified
INDEFINABLE = b'i'  # Not possible to classify
ERRONEOUS = b'e'    # Artefacts or erroneous images
SPHERE = b's'       # Spherical particles
COLUMN = b'c'       # Column-like particles
ROSETTE = b'r'      # Rosettes
DENDRITE = b'd'     # Dendrites
PLATE = b'p'        # Plates
