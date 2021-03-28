"""
                                           1
                111111                    1221  21
              112222111       112211 2    11222331113
             11211  1211    1122333222     12321  1211
             1221   1211    1231  1221      2321   1221
             1221   1221    1232  1221      2321   1121
             1221  11221    1231   2321     13211  113
             1112211211     1121  12321    1123332111
               111111        111211 121    1123211
                                            1221    1
                                            121
                                            111
                                             1
____________________________________________________________________
"""

# Importing the C++ extension (oap.core)
try:
    from __oap_c.core import (
        decompress,
        OpticalArray
    )
except ModuleNotFoundError:
    error_msg = "C extension of oap library is not compiled yet!"
    print("Catching ModuleNotFoundError:", error_msg)

from oap.__conf__ import (
    __version__,
    UNDEFINED,
    INDEFINABLE,
    ERRONEOUS,
    SPHERE,
    COLUMN,
    ROSETTE,
    DENDRITE,
    PLATE,
)
from oap.lib.imagefile import Imagefile, load_imagefile
from oap.utils import (
    barycenter,
    adjust_y,
    center_particle,
    clip_y,
    flip_x,
    flip_y,
    monochromatic,
    monoscale,
    move_to_x,
    move_to_y,
)
from oap.utils.bytes import read_particle_type
from oap.utils.console import print_array, print_separator
from oap.utils.files import array_as_oap_file, array_as_png, filepaths, read_oap_file
from oap.utils.sizing import (
    xy_diameter,
    x_diameter,
    y_diameter,
    min_diameter,
    max_diameter,
    sphere_volume,
    sphere_surface,
    hexprism_volume,
    hexprism_surface,
)
