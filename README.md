[![license](https://img.shields.io/pypi/l/oap)](LICENSE)
[![version](https://img.shields.io/pypi/pyversions/oap)](https://pypi.python.org/pypi/oap/)
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
                                                      Version 0.0.10
Optical Array Processing (oap)
Licensed under the MIT license (see `LICENSE` file)

A transparent library for processing and analyzing individual
images of Optical Array Probes (OAPs)

Author:         Lucas Grulich (lucasgrulich@gmx.de)
Last Update:    02. September 2020
```

### Introduction

The [__oap__ library](https://pypi.python.org/pypi/oap/) is a transparent tool for working directly with image data from [Optical Array Probes](https://www.eol.ucar.edu/instruments/two-dimensional-optical-array-cloud-probe).
It was initially developed for the preparation and classification of image data with neural networks.

__This software will be continuously developed further!__ Comments on this project are welcome! If you have any suggestions for improvement, you can simply write me an [email](mailto:lucasgrulich@gmx.de) and I will try to implement them.

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
import oap

images = []
oap.imagefile("Imagefile20200830120000", images=images)

for image in images[:100]:
    oap.print_array(image)
```

### Initialization & Compilation by yourself

#### Prerequisites

* Python >= 3.7
* Pipenv

```bash
pipenv install
```

```bash
python setup.py install
```
