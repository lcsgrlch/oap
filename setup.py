"""
Setup script to compile the oap library.
"""

from oap.__conf__ import __author__, __version__
from setuptools import Extension, find_namespace_packages, setup

import os

with open("README.md", "r") as f:
    long_description = f.read()

core = Extension(
    name="__oap_c.core",
    sources=[os.path.join("oap", "core", "c", "__init__.c")],
    language="c",
)

setup(
    name="oap",
    version=__version__,
    author=__author__,
    author_email="lucasgrulich@gmx.de",
    description="A transparent library for processing and analyzing individual images of Optical Array Probes (OAPs)",
    install_requires=[
        "numpy",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lcsgrlch/oap",
    packages=find_namespace_packages(),
    package_data={
        "oap.deep": ["models/*.hdf5"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    ext_modules=[core],
)
