/*
Python C++ Extension for working with Optical Array Probe (OAP)
imagefiles by Droplet Measurement Technologies (DMT).

Author:         Lucas Tim Grulich
Created:        October 2017
Last Update:    October 2017
*/



#include <Python.h>

#include <iostream>
#include <fstream>
#include <string>
using namespace std;


#include <time.h>

#include "conf.h"
#include "helpers.h"



const char *MONTH[] = {"January", "February", "March", "April",
                       "May", "June", "July", "August", "September",
                       "October", "November", "December"};

const char *GRAY_HEADER[] = {"SecOfDay", "Prtcl#", "N_y", "N_x",
                             "MilliSec", "MicroSec", "NanoSec",
                             "Min_idx", "Max_idx", "#pxl",
                             "1pxl", "2pxl", "3pxl", "TAS",
                             "N_Poisson"};

const char *MONO_HEADER[] = {"SecOfDay", "Prtcl#", "N_y", "N_x",
                             "MilliSec", "MicroSec", "Min_idx",
                             "Max_idx", "#pxl", "N_Poisson"};






void
decompress_grayscale_data(unsigned char *data,
                          int *particle_counter,
                          int *biterror_counter,
                          int *zropxels_counter,
                          int *trncated_counter,
                          PyObject *timeframes,
                          PyObject *ysizes,
                          PyObject *xsizes,
                          int truncatedparticles,
                          int centerparticle,
                          int poissonspots,
                          const char *logfilepath,
                          const char *exportdir,
                          const char *exporttype,
                          PyObject *outputlist,
                          PyObject *imageslist)
{
    /*
    Loop through compressed data to count the number of decompressed bits and
    create a stack memory with corresponding length to store the decompressed bits.
    */
    int bit_count = count_graysc_bits(data);
    unsigned char *bit_array;
    bit_array = new unsigned char[bit_count];

    int no_of_repeats = 0;
    int last_2_bits = 0;
    int current_bit = 0;

    // --- Decompress grayscale imagefile data ------------------------------------------

    /*
    Decompression algorithm of OAP grayscale imagefile data bytes.
    -> 128 bits per data slice
    */
    for (int i=0; i<4096; i++)
    {
        if (data[i]&128)
        {
            if (data[i]&128)
            {
                no_of_repeats = (data[i] & 127);
                for (int j=0; j<no_of_repeats; j++)
                {
                    if (last_2_bits == 3)
                    {
                        bit_array[current_bit++] = 1;
                        bit_array[current_bit++] = 1;
                    }
                    else if (last_2_bits == 2)
                    {
                        bit_array[current_bit++] = 1;
                        bit_array[current_bit++] = 0;
                    }
                    else if (last_2_bits == 1)
                    {
                        bit_array[current_bit++] = 0;
                        bit_array[current_bit++] = 1;
                    }
                    else
                    {
                        bit_array[current_bit++] = 0;
                        bit_array[current_bit++] = 0;
                    }
                }
            }
        }
        else
        {
            last_2_bits = (data[i] & 3);
            if (data[i]&64)
            {
                for (int j = 5; j >= 0; j--)
                {
                    if (((data[i]&63) & (1 << j)) != 0)
                        bit_array[current_bit++] = 1;
                    else
                        bit_array[current_bit++] = 0;
                }
            }
            else if (data[i]&16)
            {
                for (int j = 3; j >= 0; j--)
                {
                    if (((data[i]&15) & (1 << j)) != 0)
                        bit_array[current_bit++] = 1;
                    else
                        bit_array[current_bit++] = 0;
                }
            }
            else if (data[i]&4)
            {
                for (int j = 1; j >= 0; j--)
                {
                    if (((data[i]&3) & (1 << j)) != 0)
                        bit_array[current_bit++] = 1;
                    else
                        bit_array[current_bit++] = 0;
                }
            }
        }
    }
    // --- Find first index of decompressed data ----------------------------------------

    /*
    Imagefile data is mostly broken. Usually it does not start
    with the first particle image. Search for succesive 256 one bits
    and find the actual start of the first particle image.
    */
    int start_index;
    int succesive_ones = 0;
    bool contains_particles = false;

    for (int i=0; i<bit_count; i++)
    {
        if (succesive_ones >= 256 && bit_array[i] == 0)
        {
            start_index = i;
            contains_particles = true;
            break;
        }
        if (bit_array[i] == 1)
            succesive_ones++;
        else
            // Reset one counter.
            succesive_ones = 0;
    }
    /*
    There are data blocks in imagefiles, which do not contain any
    particles (mostly in the beginning and the end of an imagefile).
    If the data block contains particles continue with processing
    particle data.
    */
    if (! contains_particles) return;

    // --- Loop through particle data ---------------------------------------------------

    int number_of_slices = (bit_count-start_index) / 128;
    int i = 0;

    while (i<number_of_slices)
    {
        // --- Decoding particle header -------------------------------------------------

        /*
        Imagefile data bits are pairwise reversed. To decode the
        particle header it is necessary to swap the bits.
        */
        int swap_bit;
        for (int j=56; j<128; j+=2)
        {
            swap_bit = bit_array[(i*128)+j+start_index];
            bit_array[(i*128)+j+start_index] = bit_array[(i*128)+j+start_index+1];
            bit_array[(i*128)+j+start_index+1] = swap_bit;
        }

        /*
        -----------------------------------------
        Header Bits:

        0   - 56   56 bits of zeroes
        56  - 64   8  bits true air speed (TAS)
        64  - 80   16 bits particle counter
        80  - 83   3  bits nanosecond
        83  - 93   10 bits microsecond
        93  - 103  10 bits millisecond
        103 - 109  6  bits second
        109 - 115  6  bits minute
        115 - 120  5  bits hour
        120 - 127  8  bits slice count
        -----------------------------------------
        */
        unsigned char binary[16];

        int k=0;
        for (int j=120; j<128; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int particle_slices = bin_to_dec(binary, 8);



        /*
        Particle images can be broken at the end of OAP imagefile data.
        These particles are not valid, because of the missing trailer slice.
        */
        if ((i+particle_slices)*128+128+start_index >= bit_count) return;

        /*
        Every valid particle image must have 56 succesive zeros in the
        beginning (start of particle header) and 128 succesive ones in
        the end. If not the whole data buffer is probably corrupted.
        */
        for (int j=0; j<56; j++)
        {
            if (bit_array[(i*128)+j+start_index] != 0)
            {
                *biterror_counter += 1;
                return;
            }
        }
        for (int j=0; j<128; j++)
        {
            if (bit_array[((i+particle_slices)*128)+j+start_index] != 1)
            {
                *biterror_counter += 1;
                return;
            }
        }



        // --- Timestamp and True Air Speed ---------------------------------------------
        k=0;
        for (int j=115; j<120; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int hour = bin_to_dec(binary, 5);

        k=0;
        for (int j=109; j<115; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int minute = bin_to_dec(binary, 6);

        k=0;
        for (int j=103; j<109; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int second = bin_to_dec(binary, 6);

        k=0;
        for (int j=93; j<103; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int millisec = bin_to_dec(binary, 10);

        k=0;
        for (int j=83; j<93; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int microsec = bin_to_dec(binary, 10);

        k=0;
        for (int j=80; j<83; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int nanosec = bin_to_dec(binary, 3);

        k=0;
        for (int j=64; j<80; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int particle_number = bin_to_dec(binary, 16);

        k=0;
        for (int j=56; j<64; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int true_air_speed = bin_to_dec(binary, 8);



        // --- Increment Bit Array Index ------------------------------------------------
        /*
        After reading the particle header increment the current data slice
        to set the bit_array index to the current particle image data.
        */
        i++;



        /*
        The image height is the number of particle slices minus 1
        to deduct the length of the boundary trailer slice.
        The image height is equal to the particle size in
        y direction (height).
        */
        int img_height = particle_slices-1;

        // The second of day is the particle timestamp in seconds.
        int second_of_day = hour*3600 + minute*60 + second;



        bool do_stuff_with_particle = true;

        // --- Check timeframes ---------------------------------------------------------

        if (PyList_Size(timeframes))
        {
            if (! check_if_value_is_in_boundaries(second_of_day, timeframes)) {
                do_stuff_with_particle = false;
            }
        }

        // --- Check particle size in Y-axis --------------------------------------------

        if (PyList_Size(ysizes))
        {
            if (! check_if_value_is_in_boundaries(img_height, ysizes)) {
                do_stuff_with_particle = false;
            }
        }

        if (! do_stuff_with_particle)
        {
            i += particle_slices+1;
            continue;
        }



        // --- Create the particle array ------------------------------------------------

        /*
        Translate the actual particle image into a 1 dimensional single array.
        Count pixels and find the minimum and maximum index.
        */
        unsigned char *particle_array;
        particle_array = (unsigned char*) calloc(img_height*64, sizeof(unsigned char));

        int min_index = 63;
        int max_index = 0;
        int counter_1_pixels = 0;
        int counter_2_pixels = 0;
        int counter_3_pixels = 0;

        // sum_x and _y will be needed to calculate the particle barycenter.
        int sum_x = 0, sum_y = 0;

        for (int y=0; y<img_height; y++)
        {
            for (int x=0; x<64; x++)
            {
                if ((bit_array[(i+y)*128+(x*2)+start_index] == 1)
                && (bit_array[(i+y)*128+(x*2)+start_index+1] == 1))
                {
                    // Not necessary, because of calloc the value is already 0.
                    // particle_array[j*64+l] = 0;
                }
                else if ((bit_array[(i+y)*128+(x*2)+start_index] == 0)
                && (bit_array[(i+y)*128+(x*2)+start_index+1] == 1))
                {
                    particle_array[y*64+x] = 1;
                    counter_1_pixels++;
                    if (min_index > x) min_index = x;
                    if (max_index < x) max_index = x;
                    sum_x += x;
                    sum_y += y;
                }
                else if ((bit_array[(i+y)*128+(x*2)+start_index] == 1)
                && (bit_array[(i+y)*128+(x*2)+start_index+1] == 0))
                {
                    particle_array[y*64+x] = 2;
                    counter_2_pixels++;
                    if (min_index > x) min_index = x;
                    if (max_index < x) max_index = x;
                    sum_x += x;
                    sum_y += y;
                }
                else if ((bit_array[(i+y)*128+(x*2)+start_index] == 0)
                && (bit_array[(i+y)*128+(x*2)+start_index+1] == 0))
                {
                    particle_array[y*64+x] = 3;
                    counter_3_pixels++;
                    if (min_index > x) min_index = x;
                    if (max_index < x) max_index = x;
                    sum_x += x;
                    sum_y += y;
                }
            }
        }


        int particle_width = max_index-min_index+1;
        int number_of_pixels = counter_1_pixels + counter_2_pixels + counter_3_pixels;

        if (! number_of_pixels)
        {
            *zropxels_counter += 1;
            do_stuff_with_particle = false;
        }

        // --- Exclude truncated images -------------------------------------------------

        if (min_index == 0 || max_index == 63)
        {
            *trncated_counter += 1;
            if (! truncatedparticles)
            {
                do_stuff_with_particle = false;
            }
        }

        // --- Check particle size in X-axis --------------------------------------------

        if (PyList_Size(xsizes))
        {
            if (! check_if_value_is_in_boundaries(particle_width, xsizes)) {
                do_stuff_with_particle = false;
            }
        }

        if (! do_stuff_with_particle)
        {
            i += particle_slices+1;
            continue;
        }






        // --- Do stuff with particle image ---------------------------------------------

        /*
        Size of the Poisson Spot -> Zero indicates there is either no spot
        or no closed circle around the Poisson Spot.
        */
        int poisson_size = 0;

        // Calculate the barycenter of the particle image.
        int x_bary = (int) round(sum_x / (float) number_of_pixels);
        int y_bary = (int) round(sum_y / (float) number_of_pixels);



        // --- Poisson Spot Detection ---------------------------------------------------

        if (poissonspots && img_height >= 3
                         && particle_width >= 3
                         && number_of_pixels >= 4)
        {
            /*
            If the value of a bary center of a particle image is not equal
            to zero, check the adjoining pixels. If pixel value is equal to
            zero mark them with a Poisson Spot marker.
            */
            if (particle_array[y_bary*64+x_bary] != 0)
            {
                if (y_bary+1 < img_height)
                    poisson_spot(particle_array, x_bary+1, y_bary,
                                 img_height, min_index, max_index);
                if (y_bary-1 >= 0)
                    poisson_spot(particle_array, x_bary-1, y_bary,
                                 img_height, min_index, max_index);
                if (x_bary+1 < 64)
                    poisson_spot(particle_array, x_bary, y_bary+1,
                                 img_height, min_index, max_index);
                if (x_bary-1 >= 0)
                    poisson_spot(particle_array, x_bary, y_bary-1,
                                 img_height, min_index, max_index);
            }
            else
            {
                poisson_spot(particle_array, x_bary, y_bary,
                             img_height, min_index, max_index);
            }
            /*
            Measure the Poisson Spot size and remove marker, if the circle
            around the spot is not closed.
            */
            evaluate_poisson_spot(particle_array, img_height,
                                  min_index, max_index, &poisson_size);
        }



        // --- Center the particle image ------------------------------------------------

        if (centerparticle)
        {
            int ximg_center = (int) (64 / 2.0 - 0.5);
            int x_shift = ximg_center - x_bary;

            if (x_shift)
            {
                unsigned char *centered_array;
                centered_array = new unsigned char[img_height*64];

                for (int j=0; j<img_height*64; j++)
                {
                    centered_array[j] = 0;
                }
                for (int y=0; y<img_height; y++)
                {
                    for (int x=0; x<64; x++)
                    {
                        if (particle_array[y*64+x] != 0)
                        {
                            /*
                            Pixels which get pushed out of the picture frame, will
                            appear on the other side of the picture. Therefore this
                            method should be used with caution. Truncated and really
                            big images, should not get centered.
                            */
                            int new_x = (x+x_shift) % 64;
                            centered_array[y*64+new_x] = particle_array[y*64+x];
                        }
                    }
                }
                // Replace the particle array with the new centered array.
                copy(centered_array, centered_array+img_height*64, particle_array);
            }
        }



        // --- Export particles ---------------------------------------------------------

        if (strlen(exporttype))
        {
            // Concat export directory and the file name.
            string export_path(exportdir);
            export_path.append(to_string(second_of_day));
            export_path.append("_");
            export_path.append(to_string(particle_number));


            if (! strncmp(exporttype, "bin", 3))
            {
                export_path.append(".bin");

                export_particle_as_binary(particle_array,
                                          export_path.c_str(),
                                          "u", 1, img_height, 64);
            }
            else if (! strncmp(exporttype, "csv", 3))
            {
                export_path.append(".csv");

                int csv_header_values[] = {second_of_day,
                                           particle_number,
                                           img_height,
                                           particle_width,
                                           millisec,
                                           microsec,
                                           nanosec,
                                           min_index,
                                           max_index,
                                           number_of_pixels,
                                           counter_1_pixels,
                                           counter_2_pixels,
                                           counter_3_pixels,
                                           true_air_speed,
                                           poisson_size};
                int header_length = 14;
                if (poissonspots)
                {
                    header_length = 15;
                }
                export_particle_as_csv(particle_array,
                                       export_path.c_str(),
                                       GRAY_HEADER, csv_header_values,
                                       header_length, img_height, 64);
            }
        }



        // --- Print to logfile ---------------------------------------------------------

        if (strlen(logfilepath))
        {
            FILE *logfile;
            logfile = fopen(logfilepath, "a");
            fprintf(logfile,
                    "%d,%d,%d,%d,%d,"
                    "%d,%d,%d,%d,%d,"
                    "%d,%d,%d,%d",
                    second_of_day,
                    particle_number,
                    img_height,
                    particle_width,
                    millisec,
                    microsec,
                    nanosec,
                    min_index,
                    max_index,
                    number_of_pixels,
                    counter_1_pixels,
                    counter_2_pixels,
                    counter_3_pixels,
                    true_air_speed);
            if (poissonspots)
            {
                fprintf(logfile, ",%d", poisson_size);
            }
            fprintf(logfile, "\n");
            fclose(logfile);
        }



        // --- Output as PyList ---------------------------------------------------------

        if (PyList_Check(outputlist))
        {
            PyObject *output_as_list = PyList_New(0);

            PyList_Append(output_as_list, PyLong_FromLong(second_of_day));
            PyList_Append(output_as_list, PyLong_FromLong(particle_number));
            PyList_Append(output_as_list, PyLong_FromLong(img_height));
            PyList_Append(output_as_list, PyLong_FromLong(particle_width));
            PyList_Append(output_as_list, PyLong_FromLong(true_air_speed));

            PyList_Append(outputlist, output_as_list);
            Py_DECREF(output_as_list);
        }

        if (PyList_Check(imageslist))
        {
            PyObject *particle_as_list = PyList_New(0);
            for (int j=0; j<img_height; j++)
            {
                for (int l=0; l<64; l++)
                {
                    PyList_Append(particle_as_list,
                                  PyLong_FromLong(particle_array[j*64+l]));
                }
            }
            PyList_Append(imageslist, particle_as_list);
            Py_DECREF(particle_as_list);
        }

        // --- Stop doing stuff with particle image -------------------------------------






        *particle_counter += 1;

        // free() is faster than delete[].
        free(particle_array);
        /*
        +1 for the trailer boundary slice. Grayscale data has two, but
        just one is included in the slice counter of the particle header.
        */
        i += particle_slices+1;
    }
}











void
decompress_monoscale_data(unsigned char * data)
{
    int byte_count = count_monosc_bytes(data);
    unsigned char *byte_array;
    byte_array = new unsigned char[byte_count];

    int i = 0;
    int k = 0;

    bool start_recording = false;
    int boundary_count = 0;
    int start_index = 0;

    /*
    Its not likely but to make sure there is no boundary slice or
    something else in the end of the stack memory, which can be falsely
    interpreted as valid data, the memory will be set to 0.
    */
    for (int j=0; j<byte_count; j++) byte_array[j] = 0;

    while (i < 4096)
    {
        int count = (data[i]&31);

        if (data[i]&32) i++;

        else if (data[i]&128)
        {
            for (int j=0; j<count+1; j++)
            {
                if (start_recording) byte_array[k++] = 0;
                else start_index++;
            }
            i++;
        }
        else if (data[i]&64)
        {
            for (int j=0; j<count+1; j++)
            {
                if (start_recording) byte_array[k++] = 255;
                else start_index++;
            }
            i++;
        }
        else
        {
            i++;
            for (int j=0; j<count+1; j++)
            {
                if (!start_recording)
                {
                    start_index++;
                    /*
                    Count succesive 1 and 0 bits.
                    -> 8 bytes equal to 170 dec and AA hex.
                    */
                    if (data[i+j]==170)
                        boundary_count++;
                    else
                        boundary_count = 0;
                    if (boundary_count == 8)
                        start_recording = true;
                }
                else
                {
                    byte_array[k++] = data[i+j];
                }
            }
            i += count+1;
        }
    }



    /*
    After the decompression start with analyzing the
    decompressed monoscale data.
    */

    int number_of_slices = (byte_count-start_index) / 8;
    i = 0;
    // ----------------------------------------------------------------------------------- Moeglicherweise nicht perfekt
    while (i < number_of_slices)
    {
        /*
        Translating the particle header. The monoscale particle header has a
        really strange format.

        Monoscale Particle Header (8 bytes):

        Bytes:  b1 b0       b6 b5 b4 b3 b2                  b7
                -----       --------------      Bits: 0 1 2 3 4 5 6      7
                  |                |                  -------------      -
                  |                |                        |            |
                  V                V                        V            V
           particle number     timestamp            number of slices    DOF


        The timestamp is even stranger and probably better to understand by just
        looking at the code.
        */
        /*
        unsigned short b0 = byte_array[i*8+1];
        unsigned short b1 = byte_array[i*8];

        unsigned short b2 = byte_array[i*8+2];
        unsigned short b3 = byte_array[i*8+3];
        unsigned short b4 = byte_array[i*8+4];
        unsigned short b5 = byte_array[i*8+5];
        unsigned short b6 = byte_array[i*8+6];
        */



        //unsigned short particle_number = (b0 << 8) + b1;
        unsigned short particle_slices = ((byte_array[i*8+7]&254)>>1);

        /*
        Timestamp (Header Bytes):

        Byte 6      Byte 5      Byte 4      Byte 3      Byte 2
        11111|000   000|11111   1|0000000   000|11111   11111111
        -----|---------|---------|-------------|----------------
        Hour | Minute  |Second   |Milli Second |Micro Second

        */
        /*
        unsigned short hour = (b6 >> 3) & 31;
        unsigned short minute = (((b6 << 8) + b5) >> 5) & 63;
        unsigned short second = (((b5 << 8) + b4) >> 7) & 63;
        unsigned short millisec = (((b4 << 8) + b3) >> 5) & 1023;
        // multiply with 125 * 0.001 to covert it to microseconds.
        double microsec = ((((b3 << 8) + b2) >> 5) & 8191)*125 * 0.001;
        */


        /*
        Increment the index to the beginning of the actual
        image data of the particle.
        */
        i++;

        int img_height = particle_slices-1;

        int min_index = 63;
        int max_index = 0;
        int pixel_no = 0;

        unsigned char *particle_array;
        particle_array = (unsigned char*) calloc(img_height*64, sizeof(unsigned char));

        for (int j=0; j<img_height; j++)
        {
            for (int l=7; l>=0; l--)
            {
                for (int m=0; m<8; m++)
                {
                    if (byte_array[(j+i)*8+l] & ((unsigned char) pow(2, m)))
                    {
                        // Not necessary, because of calloc the value is already 0.
                        // particle_array[j*64+l*8+(7-m)] = 0;
                    }
                    else
                    {
                        particle_array[j*64+l*8+(7-m)] = MONOSC_SHADOWLEVEL;
                        if (min_index > l*8+(7-m)) min_index = l*8+(7-m);
                        if (max_index < l*8+(7-m)) max_index = l*8+(7-m);
                        pixel_no++;
                    }
                }
            }
        }





        // Do stuff with particle array!





        free(particle_array);
        i += particle_slices;
    }
}













static PyObject *
_process_imagefile(PyObject *module,
                   PyObject *args,
                   PyObject *kwargs)
{
    // Record time for runtime measurement.
    clock_t begin = clock();



    // fpath is the only non variable argument.
    const char *fpath;

    // Default values.
    const char *channel = "gray";
    const char *logfile_path = "";
    const char *export_dir = "";
    const char *export_type = "";

    int truncated_particles = 0;
    int center_particle = 0;
    int poisson_spots = 0;
    int show_bufferID = 0;
    int std_out = 0;

    PyObject *exclude_buffers = PyList_New(0);
    PyObject *include_buffers = Py_None;
    PyObject *timeframes = PyList_New(0);
    PyObject *y_sizes = PyList_New(0);
    PyObject *x_sizes = PyList_New(0);

    PyObject *output_list = Py_None;
    PyObject *images_list = Py_None;


    // Parameter keyword list.
    static char *kwlist[] = {
        "file",
        "channel",
        "logfile",
        "exportdir",
        "export",
        "truncated",
        "centerparticle",
        "poisson",
        "showbufferID",
        "stdout",
        "excludebuffers",
        "includebuffers",
        "timeframes",
        "ysizes",
        "xsizes",
        "output",
        "images",
        NULL
    };

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ssssiiiiiO!O!O!O!O!O!O!", kwlist,
                                     &fpath, &channel,
                                     &logfile_path, &export_dir, &export_type,
                                     &truncated_particles, &center_particle,
                                     &poisson_spots, &show_bufferID, &std_out,
                                     &PyList_Type, &exclude_buffers,
                                     &PyList_Type, &include_buffers,
                                     &PyList_Type, &timeframes,
                                     &PyList_Type, &y_sizes,
                                     &PyList_Type, &x_sizes,
                                     &PyList_Type, &output_list,
                                     &PyList_Type, &images_list))
    {
        PyErr_Print();
        Py_RETURN_NONE;
    }



    FILE *imagefile = fopen(fpath, "rb");

    if (imagefile == NULL)
    {
        PyErr_SetString(PyExc_IOError, "no imagefile");
        PyErr_Print();
        Py_RETURN_NONE;
    }



    // --- Create logfile and write header ----------------------------------------------

    if (strlen(logfile_path))
    {
        FILE *logfile;
        logfile = fopen(logfile_path, "w");

        if (! strncmp(channel, "gray", 4) || ! strncmp(channel, "grey", 4))
        {
            int header_length = 14;
            if (poisson_spots)
                header_length = 15;
            for (int i=0; i<header_length; i++)
            {
                fprintf(logfile, "%s", GRAY_HEADER[i]);
                if (i != header_length-1)
                    fprintf(logfile, ",");
            }
        }
        else if (! strncmp(channel, "mono", 4))
        {
            int header_length = 9;
            if (poisson_spots)
                header_length = 10;
            for (int i=0; i<header_length; i++)
            {
                fprintf(logfile, "%s", MONO_HEADER[i]);
                if (i != header_length-1)
                    fprintf(logfile, ",");
            }
        }
        fprintf(logfile, "\n");
        fclose(logfile);
    }



    /*
    Measure the number of bytes in the imagefile.
    Seek the end of file and set the index back to the top.
    */
    fseek(imagefile, 0, SEEK_END);
    long file_bytes = ftell(imagefile);
    fseek(imagefile, 0, SEEK_SET);

    /*
    OAP imagefiles consist of header (16 bytes) and data (4096 bytes)
    blocks in alternating order. If the number of bytes is not completely
    divisible by 4112 the imagefile is corrupted.
    */
    long file_length = file_bytes / 4112;
    unsigned char header[16];
    unsigned char buffer[4096];



    /*
    Number of imagefile particles, biterrors in the particle header,
    zero pixel images and truncated particle images.
    */
    int particle_counter = 0;
    int biterror_counter = 0;
    int zropxels_counter = 0;
    int trncated_counter = 0;


    for(long i=0; i<file_length; i++)
    {
        fread(header, 1, 16, imagefile);
        fread(buffer, 1, 4096, imagefile);

        if (i == 0) {
            /*
            Decode first Buffer Header to obtain the date
            (it is unlikely that the month in a flight changes).
            */
            // Bytes in the header are swapped.
            int year = (header[1] << 8 | header[0]);
            int month = (header[3] << 8 | header[2]);
            int day = (header[5] << 8 | header[4]);
            // int header_hour = header[7] << 8 | header[6];

            if (std_out)
            {
                PySys_WriteStdout("Recorded on %s %d, %d \n\n",
                                  MONTH[month-1], day, year);

                PySys_WriteStdout("File Bytes:\t%ld\n",
                                  file_bytes);
                PySys_WriteStdout("File Buffer:\t%ld\n",
                                  file_length);
                if (show_bufferID)
                    PySys_WriteStdout("\n");
            }
        }



        // --- Decompress data buffer ---------------------------------------------------

        if (! check_if_value_is_in_list(i, exclude_buffers) && check_if_value_is_in_list(i, include_buffers))
        {
            if (show_bufferID)
                PySys_WriteStdout("Data Buffer:\t%ld\n", i);

            // Check which decompressing algorithm is necessary.
            if (! strncmp(channel, "gray", 4)
            || ! strncmp(channel, "grey", 4))
            {
                decompress_grayscale_data(buffer,
                                          &particle_counter,
                                          &biterror_counter,
                                          &zropxels_counter,
                                          &trncated_counter,
                                          timeframes,
                                          y_sizes,
                                          x_sizes,
                                          truncated_particles,
                                          center_particle,
                                          poisson_spots,
                                          logfile_path,
                                          export_dir,
                                          export_type,
                                          output_list,
                                          images_list);
            }
            else if (! strncmp(channel, "mono", 4))
            {
                decompress_monoscale_data(buffer);
            }
        }
    }

    fclose(imagefile);

    if (stdout)
    {
        PySys_WriteStdout("\nParticles:\t%d\n", particle_counter);
        PySys_WriteStdout("Biterrors:\t%d\n", biterror_counter);
        PySys_WriteStdout("No Pixels:\t%d\n", zropxels_counter);
        PySys_WriteStdout("Truncated:\t%d\n", trncated_counter);

        double time_spent = (double)(clock() - begin) / CLOCKS_PER_SEC;
        PySys_WriteStdout("Runtime:\t%f seconds\n\n", time_spent);
    }

    return PyLong_FromLong(particle_counter);
}






static PyObject *
_number_of_buffers(PyObject *module,
                   PyObject *args)
{
    const char *fpath;

    if (!PyArg_ParseTuple(args, "s|", &fpath))
    {
        PyErr_Print();
        Py_RETURN_NONE;
    }

    FILE *imagefile = fopen(fpath, "rb");

    if (imagefile == NULL)
    {
        PyErr_SetString(PyExc_IOError, "no imagefile");
        PyErr_Print();
        Py_RETURN_NONE;
    }

    /*
    Measure the number of bytes in the imagefile.
    */
    fseek(imagefile, 0, SEEK_END);
    long file_bytes = ftell(imagefile);
    fclose(imagefile);

    /*
    Data Buffers of Imagfiles consists of 4112 Bytes.
    */
    long file_length = file_bytes / 4112;

    return PyLong_FromLong(file_length);
}






/* --- Module + Method Initialization --------------------------------------- */
static PyMethodDef ExtensionMethods[] = {
    /* Library Method Name, Function Name, Arguments, Description */
    {"imagefile", (PyCFunction)_process_imagefile,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"number_of_buffers", (PyCFunction)_number_of_buffers,
     METH_VARARGS, ""},
    /* Sentinel */
    {NULL, NULL, 0, NULL}
};

/* --- Module entry point Python 3 ------------------------------------------ */
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "factory",  /* name of module */
    NULL,           /* module documentation, may be NULL */
    -1,             /* size of per-interpreter state of the module,
                       or -1 if the module keeps state in global variables. */
    ExtensionMethods
};

PyMODINIT_FUNC PyInit_factory(void)
{
    return PyModule_Create(&module);
}
