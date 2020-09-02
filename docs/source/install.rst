.. _install:

Download and Install
====================

You can always download the latest releases of **oap** from the project's
`github page <https://github.com/lcsgrlch/oap>`_. The project is also on `PyPI <http://pypi.python.org/pypi/oap>`_ so the easiest way to install it is as follows:
::
    pip install oap

I always recommend the use of virtual environments (e.g. `venv <https://docs.python.org/3/library/venv.html>`_ & `pipenv <https://github.com/pypa/pipenv>`_ to avoid destroying your Python installation.

But if you don't want to work with virtual environments and still don't want to mess up your system directories, install the library as a user:
::
    pip install oap --user


Platforms and Interpreters
--------------------------

The latest release supports:

* **Python** >= 3.7
* May also work on 3.5 and 3.6 (not tested)

The **oap** library is **not** a pure-python library. Decompression algorithms and some other methods are written in C++.
However, this project uses `Python Wheels <https://pythonwheels.com/>`_ and was pre-compiled for 64-bit architectures on following operating systems:

* Windows 10

Anyway, if you want to use **oap** on a 32-bit architecture you need to compile the project first.
Just clone the project from github and compile & install:
::
    git clone ???
    cd oap
    python setup.py install
