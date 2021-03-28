/*
Python C++ Extension for working with Optical Array Probe (OAP)
imagefiles by Droplet Measurement Technologies (DMT).

Author:         Lucas Tim Grulich
Created:        October 2017
Last Update:    March 2021
*/
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>

#define _USE_MATH_DEFINES
#include <math.h>
#include <structmember.h>

#include "utils.h"
#include "opticalarray.h"
#include "poisson.h"
#include "principal.h"
#include "cluster.h"
#include "processing.h"
#include "decompress.h"



static PyMethodDef core_methods[] = {
    {"decompress", (PyCFunction) decompress, METH_VARARGS | METH_KEYWORDS, ""},
    {NULL}  /* Sentinel */
};

static PyModuleDef core_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "__oap_c.core",
    .m_doc = "",    // ToDo: missing short description
    .m_size = -1,
    .m_methods = core_methods,
};

PyMODINIT_FUNC PyInit_core(void)
{
    PyObject *m;

    m = PyModule_Create(&core_module);
    if (m == NULL)
        return NULL;

    if (PyType_Ready(&OpticalArrayType) < 0)
        return NULL;

    Py_INCREF(&OpticalArrayType);
    if (PyModule_AddObject(m, "OpticalArray", (PyObject *) &OpticalArrayType) < 0) {
        Py_DECREF(&OpticalArrayType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
