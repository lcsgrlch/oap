/*
Utility methods for the core library.
*/



int
count_grayscale_bits(unsigned char *data)
{
    /*
    Counts the number of decompressed BITs in a compressed
    grayscale byte array.
    */
    int bit_counter = 0;
    for (int i=0; i<4096; i++)
    {
        if (data[i]&128)
            bit_counter += 2*(data[i]&127);
        else
        {
            if      (data[i]&64) bit_counter += 6;
            else if (data[i]&16) bit_counter += 4;
            else if (data[i]&4)  bit_counter += 2;
        }
    }
    return bit_counter;
}



int
count_monoscale_bytes(unsigned char *data)
{
    /*
    Counts the number of decompressed BYTEs in a compressed
    monoscale byte array.
    */

    int byte_counter = 0;
    int i = 0;

    while (i < 4096)
    {
        int count = (data[i]&31);
        if (data[i]&32)
        {
            i++;
        }
        else if (data[i]&128 || data[i]&64)
        {
            byte_counter += count+1;
            i++;
        }
        else
        {
            byte_counter += count+1;
            i += count+2;
        }
    }
    return byte_counter;
}



int
bin_to_dec(unsigned char *bin, int length)
{
    /*
    Fast method to convert a binary value to
    an integer value.

    The binary order is reversed:

    unsigned char bin[3] = {0,0,1};
    bin_to_dec(bin, 3); // Result: 4
    */
    int dec = 0;
    for (int i=0; i<length; i++)
    {
        if (bin[i])
        {
            dec |= (1 << (i));
        }
    }
    return dec;
}



bool
check_if_value_is_in_list(long value, PyObject *list)
{
    /*
    Method to check if a value lies in a Python list object.

    Just like the Python code: (value in list)
    */

    // If there is no valid list return true.
    if (! PyList_Check(list))
        return true;

    Py_ssize_t list_size = PyList_Size(list);
    bool value_in_list = false;

    for (int i=0; i<list_size; i++)
    {
        long list_element = PyLong_AsLong(PyList_GetItem(list, i));

        if (value == list_element)
        {
            value_in_list = true;
        }
    }
    return value_in_list;
}



bool
check_if_value_is_in_boundaries(long value, PyObject *tuples)
{
    /*
    Method to check if a value lies in specific boundaries.
    */

    if (! PyList_Check(tuples))
        return true;

    if (! PyList_Size(tuples))
        return true;

    Py_ssize_t number_of_tuples = PyList_Size(tuples);
    bool value_in_tuples = false;

    for (int i=0; i<number_of_tuples; i++)
    {
        PyObject * tuple = PyList_GetItem(tuples, i);   // ToDo: Py_DECREF tuple?

        if (PyTuple_Check(tuple))
        {
            long min_boundary = PyLong_AsLong(PyTuple_GetItem(tuple, 0));
            long max_boundary = PyLong_AsLong(PyTuple_GetItem(tuple, 1));

            if (value >= min_boundary && value <= max_boundary)
            {
                value_in_tuples = true;
            }
        }
    }
    return value_in_tuples;
}



void
print_array(unsigned char *array, int number_of_slices, int slice_size)
{
    for (int y=0; y<number_of_slices; y++)
    {
        for (int x=0; x<slice_size; x++)
        {
            if (array[y*slice_size+x])
                printf("%i ", array[y*slice_size+x]);
            else
                printf("  ");
        }
        printf("\n");
    }
}



void progress_bar(int iteration, int total, int length, char *prefix, char *suffix)
{
    int progress = (int) round((iteration / (float) total) * length);
    printf("\r%s[", prefix);
    printf("%.*s", progress,
    "====================================================================================================");
    printf("%.*s", length-progress,
    "....................................................................................................");
    printf("] %.1f%%%s", (iteration / (float) total) * 100.0, suffix);
    fflush(stdout);
    if (iteration == total)
        printf("\n");
}
