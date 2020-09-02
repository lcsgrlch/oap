/*
C++ methods for working with Optical Array Probe (OAP) imagefiles.

Author:         Lucas Tim Grulich
Created:        October 2017
Last Update:    October 2017
*/





int
count_graysc_bits(unsigned char * data)
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
count_monosc_bytes(unsigned char * data)
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
        if (data[i]&32) i++;

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
bin_to_dec(unsigned char * bin, int length)
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

    Py_ssize_t number_of_tuples = PyList_Size(tuples);
    bool value_in_tuples = false;

    for (int i=0; i<number_of_tuples; i++)
    {
        PyObject * tuple = PyList_GetItem(tuples, i);

        if (PyTuple_Check(tuple))
        {
            long min_boundary = PyLong_AsLong(PyTuple_GetItem(tuple, 0));
            long max_boundary = PyLong_AsLong(PyTuple_GetItem(tuple, 1));

            if (value > min_boundary && value < max_boundary)
            {
                value_in_tuples = true;
            }
        }
    }
    return value_in_tuples;
}



void
poisson_spot(unsigned char *data,
             int x, int y,
             int ysize,
             int xmin, int xmax)
{
    /*
    Checks if the value for index (y,x) is zero. If true, the pixel
    gets marked with a PoissonSpot marker.
    */

    if (x >= xmin && x <= xmax && y >= 0 && y < ysize)
    {
        if (data[y*64+x] == 0)
        {
            data[y*64+x] = POISSONSPOT_MARKER;
            poisson_spot(data, x, y+1, ysize, xmin, xmax);
            poisson_spot(data, x, y-1, ysize, xmin, xmax);
            poisson_spot(data, x+1, y, ysize, xmin, xmax);
            poisson_spot(data, x-1, y, ysize, xmin, xmax);
        }
    }
    return;
}



void
evaluate_poisson_spot(unsigned char *data,
                      int imgheight,
                      int minindex,
                      int maxindex,
                      int *poisson_size)
{
    /*
    Measures the sizes of marked Poisson Spots. If the Poisson Spot is not a closed
    circle the Poisson Spot markers will be deleted.
    The Poisson size is positive if there is a Poisson Spot with a closed circle.
    */

    int min_poisson = 63;
    int max_poisson = 0;

    bool closed_circle = true;
    bool contains_poisson_spot = false;

    /*
    Find the minimum and maximum of the Poisson Spot
    to calculate the sizes of both spots.
    */
    for (int i=0; i<imgheight; i++)
    {
        for (int j=0; j<64; j++)
        {
            if (data[i*64+j] == POISSONSPOT_MARKER)
            {
                contains_poisson_spot = true;
                if (min_poisson > j) min_poisson = j;
                if (max_poisson < j) max_poisson = j;
            }
        }
    }

    if (max_poisson >= min_poisson)
        *poisson_size = max_poisson-min_poisson+1;

    /*
    Check if the Poisson Spots are closed circles. Otherwise it is not
    possible to measure the size of the spots.
    */
    for (int x=0; x<64; x++)
    {
        if (data[x] == POISSONSPOT_MARKER || data[(imgheight-1)*64+x] == POISSONSPOT_MARKER)
        {
            closed_circle = false;
        }
    }
    for (int y=0; y<imgheight; y++)
    {
        if (data[y*64+minindex] == POISSONSPOT_MARKER || data[y*64+maxindex] == POISSONSPOT_MARKER)
        {
            closed_circle = false;
        }
    }

    /*
    If there is no closes Poisson Spot it's not possible to measure
    the spot size. Therefore the particle array will be cleaned of the
    Poisson Spot markers.
    */
    if (contains_poisson_spot && ! closed_circle) {

        // Reset the size of the PoissonSpot.
        *poisson_size = 0;

        for (int i=0; i<imgheight; i++)
        {
            for (int j=0; j<64; j++)
            {
                if (data[i*64+j] == POISSONSPOT_MARKER)
                {
                    data[i*64+j] = 0;
                }
            }
        }
    }
}



void
export_particle_as_binary(unsigned char *array,
                          const char *filepath,
                          const char *header,
                          int headerbytes,
                          int height,
                          int width)
{
    /*
    Saves decompressed OAP data as binary image.
    */

    FILE *image = fopen(filepath, "wb");

    // write header data.
    for (int i=0; i<headerbytes; i++) {
        fwrite(&header[i], sizeof(header[i]), 1, image);
    }
    // write image data.
    for (int i=0; i<height; i++) {
        for (int j=0; j<width; j++) {
            fwrite(&array[i*width+j], sizeof(array[i*width+j]), 1, image);
        }
    }
    fclose(image);
}



void
export_particle_as_csv(unsigned char *array,
                       const char *filepath,
                       const char **header,
                       int *headervalues,
                       int headerlength,
                       int height,
                       int width)
{
    /*
    Saves decompressed OAP data as csv file.
    */

    FILE *csv = fopen(filepath, "wb");

    // write header data.
    for (int i=0; i<headerlength; i++)
    {
        fprintf(csv, "%s", header[i]);
        if (i != headerlength-1) fprintf(csv, ",");
    }
    fprintf(csv, "\n");
    for (int i=0; i<headerlength; i++)
    {
        fprintf(csv, "%d", headervalues[i]);
        if (i != headerlength-1) fprintf(csv, ",");
    }
    fprintf(csv, "\n");

    // write image data.
    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width; j++)
        {
            fprintf(csv, "%d", (int) array[i*width+j]);
            if (j != width-1) fprintf(csv, ",");
        }
        fprintf(csv, "\n");
    }
    fclose(csv);
}



void
print_particle_array(unsigned char array[], int slices)
{
    /*
    Prints a particle array for debugging purposes.
    */
    for (int i=0; i<slices; i++)
    {
        for (int j=0; j<64; j++)
        {
            if (array[i*64+j])
                cout << (int) array[i*64+j] << " ";
            else
                cout << "  ";
        }
        cout << endl;
    }
}
