.. oap documentation master file, created by
   sphinx-quickstart on Sun Aug 30 19:24:47 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Optical Array Processing for Python
===================================

.. literalinclude:: ../../LOGO

Introduction
------------

The `oap <https://pypi.python.org/pypi/oap/>`_ library is a transparent tool, written in `Python <https://www.python.org/>`_ and `C <https://en.wikipedia.org/wiki/C_(programming_language)>`_, for working directly with image data from `Optical Array Probes <https://www.eol.ucar.edu/instruments/two-dimensional-optical-array-cloud-probe>`_.
It was initially developed for the preparation and classification of image data with neural networks.

**This software will be continuously developed further!** Comments on this project are welcome! If you have any suggestions for improvement, you can simply write me an `email <mailto:lucasgrulich@gmx.de>`_ and I will try to implement them.

I have already written a lot of other code that is not yet ready to be released. But little by little I will try to make the code available for everyone.

At the current state, the decompression algorithm is only available for grayscale probes by `Droplet Measurement Technologies (DMT) <https://www.dropletmeasurement.com/>`_.

* Decompression for DMT monoscale probes coming next!


Getting Started
---------------
:ref:`Installing <install>` **oap** is as easy as:
::
   pip install oap

If you’re new to the **oap** library and/or Python, be sure to check out the :ref:`Tutorial <tutorial>` and the :ref:`Documentation <docs>`.


Contents
--------
.. toctree::
   :maxdepth: 2

   install


.. toctree::
   :maxdepth: 2

   tutorial


.. toctree::
   :maxdepth: 2

   docs

.. toctree::
   :maxdepth: 1

   license


..
   Indices and tables
   ------------------

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
