[![PyPI - License](https://img.shields.io/pypi/l/oap)](LICENSE)
[![version](https://img.shields.io/pypi/pyversions/oap)](https://pypi.python.org/pypi/oap/)
[![Documentation Status](https://readthedocs.org/projects/oap/badge/?version=latest)](https://oap.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/oap)](https://pypi.python.org/pypi/oap/)
```
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
                                                      Version 0.0.11
Optical Array Processing (oap)
Licensed under the MIT license (see `LICENSE` file)

A transparent library for processing and analyzing individual
images of Optical Array Probes (OAPs)

Author:         Lucas Grulich
Last Update:    March 28, 2021
```

### Introduction

The [__oap__](https://pypi.python.org/pypi/oap/) library is a transparent tool, written in [Python](https://www.python.org/) and [C](https://en.wikipedia.org/wiki/C_(programming_language)), for working directly with image data from [Optical Array Probes](https://www.eol.ucar.edu/instruments/two-dimensional-optical-array-cloud-probe).
It was initially developed for the preparation and classification of image data with neural networks.

__This software is still in the alpha phase and will be further developed at irregular intervals!__ Comments on this project are always welcome! If you have suggestions for improvement, you can simply write me an [email](mailto:lucasgrulich@gmx.de) and I will try to implement them.

At the current state, the decompression algorithm has only been implemented for grayscale probes by [Droplet Measurement Technologies (DMT)](https://www.dropletmeasurement.com/).

* DMT Monoscale Decompression coming next!

The complete __documentation__ can be found at https://oap.readthedocs.io

### Installation

The __oap__ library is available on [PyPi](https://pypi.python.org/pypi/oap/), so simply open a terminal window and type at the prompt:
```bash
pip install oap
```
I always recommend the use of virtual environments (e.g. [venv](https://docs.python.org/3/library/venv.html) & [pipenv](https://github.com/pypa/pipenv)) to avoid destroying your Python installation.

But if you don't want to work with virtual environments and still don't want to mess up your system directories, install the library as a user:
```bash
pip install oap --user
```

### Usage

A short code snippet that decompresses an OAP imagefile and outputs the first 100 images to the console:
```
from oap import Imagefile

imagefile = Imagefile("Imagefile20200830120000")

# search for columns and rosettes
imagefile.classify()

# plot number of particles per flight second
imagefile.plot()

# plot number of rosettes per flight second
imagefile.plot(r=(0.5, 1))

# get all optical arrays containing particles of size
# 100 to 200 micrometers (area ratio) that were recorded
# between flight seconds 20000 and 22000.
array_list = imagefile.get_arrays(timespan=(20000, 22000),
                                  area_ratio=(100, 200))

# print particle images
for array in array_list:
    array.print()
```

### Initialization & Compilation

#### Prerequisites

* Python >= 3.7
* Pipenv

```bash
pipenv install
```

```bash
python setup.py install
```
