/*

*/

typedef struct {
    PyObject_HEAD

    unsigned char *array;

    unsigned int second;
    unsigned short number;
    unsigned short millisecond;
    unsigned short microsecond;
    // unsigned char nanosecond;
    // unsigned short tas;

    unsigned char y_dim;
    unsigned char x_bary;
    unsigned char y_bary;
    unsigned char min_idx;
    unsigned char max_idx;

    // unsigned short pixel;
    unsigned short pixel_one;
    unsigned short pixel_two;
    unsigned short pixel_thr;

    unsigned char poisson;
    unsigned char poisson_mono;
    unsigned char truncated;
    unsigned char cluster;

    float hit_ratio;
    float axis_ratio;
    float alpha;
    float column;
    float rosette;

} OpticalArrayObject;



/*
 *      * ----------------------------- *
 * ---  | OpticalArray: Special Methods | ------------------------------------------------------------------------------
 *      * ----------------------------- *
 */
static PyObject *
OpticalArray_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    OpticalArrayObject *self;
    self = (OpticalArrayObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->second = 0;
        self->number = 0;
        self->millisecond = 0;
        self->microsecond = 0;
        self->y_dim = 0;
        self->x_bary = 0;
        self->y_bary = 0;
        self->min_idx = 0;
        self->max_idx = 0;
        self->pixel_one = 0;
        self->pixel_two = 0;
        self->pixel_thr = 0;
        self->poisson = 0;
        self->poisson_mono = 0;
        self->truncated = 0;
        self->cluster = 0;
        self->hit_ratio = 0;
        self->axis_ratio = 0;
        self->alpha = 0;
        self->column = 0;
        self->rosette = 0;
    }
    return (PyObject *) self;
}

static int
OpticalArray_init(OpticalArrayObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"array",
                             "second",
                             "number",
                             "millisecond",
                             "microsecond",
                             "y_dim",
                             "x_bary",
                             "y_bary",
                             "min_idx",
                             "max_idx",
                             "pixel_one",
                             "pixel_two",
                             "pixel_thr",
                             "poisson",
                             "poisson_mono",
                             "truncated",
                             "cluster",
                             "hit_ratio",
                             "axis_ratio",
                             "alpha",
                             "column",
                             "rosette",
                             NULL};

    unsigned char *buffer;  // ToDo: is this really the best solution?
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|y*IHHHbbbbbHHHbbbbfffff", kwlist,
                                     &buffer,
                                     &self->second,
                                     &self->number,
                                     &self->millisecond,
                                     &self->microsecond,
                                     &self->y_dim,
                                     &self->x_bary,
                                     &self->y_bary,
                                     &self->min_idx,
                                     &self->max_idx,
                                     &self->pixel_one,
                                     &self->pixel_two,
                                     &self->pixel_thr,
                                     &self->poisson,
                                     &self->poisson_mono,
                                     &self->truncated,
                                     &self->cluster,
                                     &self->hit_ratio,
                                     &self->axis_ratio,
                                     &self->alpha,
                                     &self->column,
                                     &self->rosette))
        return -1;
    self->array = buffer;
    return 0;
}

static void
OpticalArray_dealloc(OpticalArrayObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
OpticalArray_repr(OpticalArrayObject *self)
{
    char *image;
    image = (unsigned char*) malloc((self->y_dim * 64 + 1) * sizeof(char));

    for (int y=0; y<self->y_dim; y++)
    {
        for (int x=0; x<64; x++)
        {
            if (self->array[y*64+x] == 0)
                image[y*64+x] = " ";
            else if (self->array[y*64+x] == 1)
                image[y*64+x] = "1";
            else if (self->array[y*64+x] == 2)
                image[y*64+x] = "2";
            else if (self->array[y*64+x] == 3)
                image[y*64+x] = "3";
            else
                image[y*64+x] = "X";
        }
    }
    image[self->y_dim * 64 + 1] = NULL;
    const char * tmp = image;

    const char test[5] = "Test";
    for (int i=0; i<5; i++)
        printf("%c ", test[i]);

    PyObject *unicode = PyUnicode_FromString(test);
    free(image);
    return unicode;
}



/*
 *      * --------------------------- *
 * ---  | OpticalArray: Class Methods | --------------------------------------------------------------------------------
 *      * --------------------------- *
 */
static PyObject *
OpticalArray_width(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(self->max_idx - self->min_idx + 1);
}

static PyObject *
OpticalArray_height(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(self->y_dim);
}

static PyObject *
OpticalArray_bytes(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("y#", self->array, 64*self->y_dim);
}

static PyObject *
OpticalArray_list(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *list = PyList_New(0);
    for (int i=0; i<self->y_dim*64; i++)
        PyList_Append(list, PyLong_FromLong(self->array[i]));
    return list;
}

static PyObject *
OpticalArray_string(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    char * test = "Hallo Welt!%d";
    char * buffer;
    int result = 4;
    snprintf(buffer, 5, "%d", result);
    return Py_BuildValue("s#", buffer, strlen(buffer));
}

static PyObject *
OpticalArray_pixel(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(self->pixel_one + self->pixel_two + self->pixel_thr);
}

static PyObject *
OpticalArray_area_ratio(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    double ratio = sqrt((self->pixel_one + self->pixel_two + self->pixel_thr) * M_PI) * 15;
    return PyFloat_FromDouble(ratio);
}

static PyObject *
OpticalArray_tensor(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    int new_xbary = 31;
    int new_ybary = 31;
    float *tensor_array;
    tensor_array = (float*) calloc(64 * 64, sizeof(float));

    int y_dimension;
    if (64 > self->y_dim)
        y_dimension = self->y_dim;
    else
        y_dimension = 64;

    int x_shift = new_xbary - self->x_bary;
    int y_shift = new_ybary - self->y_bary;
    float pixel_value;

    for (int y=y_shift; y<y_dimension+y_shift; y++)
    {
        for (int x=0; x<64; x++)
        {
            pixel_value = 0.0; // ToDo: monochromatic

            if (self->array[(y-y_shift)*64+x] != 0 && self->array[(y-y_shift)*64+x] != 7) // ToDo: poisson spot
            {
                pixel_value = 1.0;
            }

            if (pixel_value != 0)
            {
                if (new_xbary != -1)
                {
                    int new_x = x+x_shift;
                    if (new_x >= 0 && new_x < 64)
                    {
                        if (y >= 0 && y < 64)
                        {
                            tensor_array[y*64+new_x] = pixel_value;
                        }
                    }
                }
                else
                {
                    if (y >= 0 && y < 64)
                        tensor_array[y*64+x] = pixel_value;
                }
            }
        }
    }

    PyObject *particle_as_tensor = PyList_New(0);
    for (int i=0; i<64*64; i++)
    {
        PyList_Append(particle_as_tensor, PyFloat_FromDouble(tensor_array[i]));
    }
    free(tensor_array);
    return particle_as_tensor;
}

static PyObject *
OpticalArray_print(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    print_array(self->array, self->y_dim, 64);
    return Py_None;
}

static PyObject *
OpticalArray_reduce(OpticalArrayObject *self, PyObject *Py_UNUSED(ignored))
{
    return Py_BuildValue("O(y#IHHHBBBBBHHHBBBBfffff)",
                         PyObject_GetAttrString(self, "__class__"),    // ToDo: is this the best way?
                         self->array, 64 * self->y_dim,
                         self->second,
                         self->number,
                         self->millisecond,
                         self->microsecond,
                         self->y_dim,
                         self->x_bary,
                         self->y_bary,
                         self->min_idx,
                         self->max_idx,
                         self->pixel_one,
                         self->pixel_two,
                         self->pixel_thr,
                         self->poisson,
                         self->poisson_mono,
                         self->truncated,
                         self->cluster,
                         self->hit_ratio,
                         self->axis_ratio,
                         self->alpha,
                         self->column,
                         self->rosette);
}

// ---------------------------------------------------------------------------------------------------------------------



static PyMemberDef OpticalArray_members[] = { // ToDo: missing descriptions!
    {"second", T_UINT, offsetof(OpticalArrayObject, second), 0, ""},
    {"number", T_USHORT, offsetof(OpticalArrayObject, number), 0, ""},
    {"hit_ratio", T_FLOAT, offsetof(OpticalArrayObject, hit_ratio), 0, ""},
    {"axis_ratio", T_FLOAT, offsetof(OpticalArrayObject, axis_ratio), 0, ""},
    {"alpha", T_FLOAT, offsetof(OpticalArrayObject, alpha), 0, ""},
    {"column", T_FLOAT, offsetof(OpticalArrayObject, column), 0, ""},
    {"rosette", T_FLOAT, offsetof(OpticalArrayObject, rosette), 0, ""},
    {"truncated", T_BOOL, offsetof(OpticalArrayObject, truncated), 0, ""},
    {NULL}  /* Sentinel */
};

static PyMethodDef OpticalArray_methods[] = { // ToDo: missing descriptions!
    {"string", (PyCFunction) OpticalArray_string, METH_NOARGS, ""},
    {"bytes", (PyCFunction) OpticalArray_bytes, METH_NOARGS, ""},
    {"list", (PyCFunction) OpticalArray_list, METH_NOARGS, ""},
    {"pixel", (PyCFunction) OpticalArray_pixel, METH_NOARGS, ""},
    {"print", (PyCFunction) OpticalArray_print, METH_NOARGS, ""},
    {"width", (PyCFunction) OpticalArray_width, METH_NOARGS, ""},
    {"height", (PyCFunction) OpticalArray_height, METH_NOARGS, ""},
    {"tensor", (PyCFunction) OpticalArray_tensor, METH_NOARGS, ""},
    {"area_ratio", (PyCFunction) OpticalArray_area_ratio, METH_NOARGS, ""},
    {"__reduce__", (PyCFunction) OpticalArray_reduce, METH_NOARGS, ""},
    {NULL}  /* Sentinel */
};

static PyTypeObject OpticalArrayType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "oap.OpticalArray",
    .tp_doc = "", // ToDo: missing descriptions!
    .tp_basicsize = sizeof(OpticalArrayObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = OpticalArray_new,
    .tp_init = (initproc) OpticalArray_init,
    .tp_dealloc = (destructor) OpticalArray_dealloc,
    .tp_repr = OpticalArray_repr,
    .tp_members = OpticalArray_members,
    .tp_methods = OpticalArray_methods,
};
