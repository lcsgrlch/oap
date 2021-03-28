/*
Decompression algorithms for different OAPs.
*/

const char *MONTH[] = {"January", "February", "March", "April",
                       "May", "June", "July", "August", "September",
                       "October", "November", "December"};



/*
 *      * --------------------------------------------------------------- *
 * ---  | DMT Cloud Imaging Probe: Monoscale Data Decompression Algorithm | --------------------------------------------
 *      * --------------------------------------------------------------- *
 */
void
decompress_monoscale_buffer(unsigned char *data)
{
    int byte_count = count_monoscale_bytes(data);
    unsigned char *byte_array;
    byte_array = (unsigned char*) malloc(byte_count * sizeof(unsigned char));

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
        unsigned short b0 = byte_array[i*8+1];
        unsigned short b1 = byte_array[i*8];

        unsigned short b2 = byte_array[i*8+2];
        unsigned short b3 = byte_array[i*8+3];
        unsigned short b4 = byte_array[i*8+4];
        unsigned short b5 = byte_array[i*8+5];
        unsigned short b6 = byte_array[i*8+6];


        //unsigned short particle_number = (b0 << 8) + b1;
        unsigned short particle_slices = ((byte_array[i*8+7]&254)>>1);

        /*
        Timestamp (Header Bytes):

        Byte 6      Byte 5      Byte 4      Byte 3      Byte 2
        11111|000   000|11111   1|0000000   000|11111   11111111
        -----|---------|---------|-------------|----------------
        Hour | Minute  |Second   |Millisecond  |Microsecond

        */
        unsigned short hour = (b6 >> 3) & 31;
        unsigned short minute = (((b6 << 8) + b5) >> 5) & 63;
        unsigned short second = (((b5 << 8) + b4) >> 7) & 63;
        unsigned short millisecond = (((b4 << 8) + b3) >> 5) & 1023;
        // multiply with 125 * 0.001 to covert it to microseconds.
        unsigned short microsecond = (unsigned short) (((((b3 << 8) + b2) >> 5) & 8191)*125 * 0.001);

        int second_of_day = hour*3600 + minute*60 + second;

        /*
        Increment the index to the beginning of the actual
        image data of the particle.
        */
        i++;

        int img_height = particle_slices-1;

        int min_index = 63;
        int max_index = 0;
        int number_of_pixels = 0;

        unsigned char *particle_array;
        particle_array = (unsigned char*) calloc(img_height*64, sizeof(unsigned char));

        for (int y=0; y<img_height; y++)
        {
            for (int x=7; x>=0; x--)
            {
                for (int z=0; z<8; z++)
                {
                    if (byte_array[(y+i)*8+x] & ((unsigned char) pow(2, z)))
                    {
                        // Not necessary, because of calloc the value is already 0.
                        // particle_array[j*64+l*8+(7-m)] = 0;
                    }
                    else
                    {
                        particle_array[y*64+x*8+(7-z)] = 1;
                        if (min_index > x*8+(7-z)) min_index = x*8+(7-z);
                        if (max_index < x*8+(7-z)) max_index = x*8+(7-z);
                        number_of_pixels++;
                    }
                }
            }
        }



        /*
         *        * ------------------------------------- *
         *  ----- | START DOING STUFF WITH PARTICLE IMAGE | ---------------------------------------------------  >>  ---
         *        * ------------------------------------- *
         */

        process_particle_array(particle_array,
                               64,
                               img_height,
                               0,
                               0,
                               second_of_day,
                               millisecond,
                               microsecond,
                               0,
                               0,
                               0,
                               0,
                               number_of_pixels,
                               min_index,
                               max_index,
                               0,
                               0,
                               false,
                               false,
                               false,
                               false,
                               NULL);

        /*
         *        * ------------------------------------ *
         *  ----- | STOP DOING STUFF WITH PARTICLE IMAGE | ----------------------------------------------------  ||  ---
         *        * ------------------------------------ *
         */



        free(particle_array);
        i += particle_slices;
    }
    free(byte_array);
}





/*
 *      * --------------------------------------------------------------- *
 * ---  | DMT Cloud Imaging Probe: Grayscale Data Decompression Algorithm | --------------------------------------------
 *      * --------------------------------------------------------------- *
 */
void
decompress_grayscale_buffer(unsigned char *data,
                            unsigned int *particle_counter,
                            unsigned int *biterror_counter,
                            unsigned int *zropxels_counter,
                            unsigned int *trncated_counter,
                            PyObject *timeframes,
                            PyObject *x_sizes,
                            PyObject *y_sizes,
                            int truncated,
                            int poisson,
                            int cluster,
                            int principal,
                            PyObject *arrays_list)
{
    /*
    Loop through compressed data to count the number of decompressed bits and
    create a stack memory with corresponding length to store the decompressed bits.
    */
    int bit_count = count_grayscale_bits(data);
    unsigned char *bit_array;
    bit_array = (unsigned char*) calloc(bit_count, sizeof(unsigned char));

    int no_of_repeats = 0;
    int last_2_bits = 0;
    int current_bit = 0;

    // --- Decompress grayscale imagefile data -------------------------------------------------------------------------

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
                        current_bit++;
                    }
                    else if (last_2_bits == 1)
                    {
                        current_bit++;
                        bit_array[current_bit++] = 1;
                    }
                    else
                    {
                        current_bit++;
                        current_bit++;
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
                        current_bit++;
                }
            }
            else if (data[i]&16)
            {
                for (int j = 3; j >= 0; j--)
                {
                    if (((data[i]&15) & (1 << j)) != 0)
                        bit_array[current_bit++] = 1;
                    else
                        current_bit++;
                }
            }
            else if (data[i]&4)
            {
                for (int j = 1; j >= 0; j--)
                {
                    if (((data[i]&3) & (1 << j)) != 0)
                        bit_array[current_bit++] = 1;
                    else
                        current_bit++;
                }
            }
        }
    }
    // --- Find first index of decompressed data -----------------------------------------------------------------------

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
    if (! contains_particles) {
        free(bit_array);
        return;
    }

    // --- Loop through particle data ----------------------------------------------------------------------------------

    int number_of_slices = (bit_count-start_index) / 128;
    int i = 0;

    while (i<number_of_slices)
    {
        // --- Decoding particle header --------------------------------------------------------------------------------

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
        if ((i+particle_slices)*128+128+start_index >= bit_count) {
            free(bit_array);
            return;
        }

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
                free(bit_array);
                return;
            }
        }
        for (int j=0; j<128; j++)
        {
            if (bit_array[((i+particle_slices)*128)+j+start_index] != 1)
            {
                *biterror_counter += 1;
                free(bit_array);
                return;
            }
        }



        // --- Timestamp and True Air Speed ----------------------------------------------------------------------------
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
        int millisecond = bin_to_dec(binary, 10);

        k=0;
        for (int j=83; j<93; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int microsecond = bin_to_dec(binary, 10);

        k=0;
        for (int j=80; j<83; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int nanosecond = bin_to_dec(binary, 3);

        k=0;
        for (int j=64; j<80; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int particle_number = bin_to_dec(binary, 16);

        k=0;
        for (int j=56; j<64; j++)
            binary[k++] = bit_array[(i*128)+j+start_index];
        int true_air_speed = bin_to_dec(binary, 8);



        // --- Increment Bit Array Index -------------------------------------------------------------------------------
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

        // --- Check timeframes ----------------------------------------------------------------------------------------

        if (! check_if_value_is_in_boundaries(second_of_day, timeframes))
        {
            do_stuff_with_particle = false;
        }

        // --- Check particle size in Y-axis ---------------------------------------------------------------------------

        if (! check_if_value_is_in_boundaries(img_height, y_sizes))
        {
            do_stuff_with_particle = false;
        }

        if (! do_stuff_with_particle)
        {
            i += particle_slices+1;
            continue;
        }



        // --- Create the particle array -------------------------------------------------------------------------------

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

        // --- Exclude truncated images --------------------------------------------------------------------------------

        int particle_truncated = 0;

        if (min_index == 0 || max_index == 63)
        {
            *trncated_counter += 1;
            particle_truncated = 1;

            if (! truncated)
            {
                do_stuff_with_particle = false;
            }
        }

        // --- Check particle size in X-axis ---------------------------------------------------------------------------

        if (! check_if_value_is_in_boundaries(particle_width, x_sizes))
        {
            do_stuff_with_particle = false;
        }

        if (! do_stuff_with_particle)
        {
            i += particle_slices+1;
            free(particle_array);
            continue;
        }

        // Calculate the barycenter of the particle image.
        int x_bary = (int) round(sum_x / (float) number_of_pixels);
        int y_bary = (int) round(sum_y / (float) number_of_pixels);



        /*
         *        * ------------------------------------- *
         *  ----- | START DOING STUFF WITH PARTICLE IMAGE | ---------------------------------------------------  >>  ---
         *        * ------------------------------------- *
         */

        process_particle_array(particle_array,
                               64,
                               img_height,
                               particle_width,
                               particle_number,
                               second_of_day,
                               millisecond,
                               microsecond,
                               nanosecond,
                               counter_1_pixels,
                               counter_2_pixels,
                               counter_3_pixels,
                               number_of_pixels,
                               min_index,
                               max_index,
                               x_bary,
                               y_bary,
                               particle_truncated,
                               poisson,
                               cluster,
                               principal,
                               arrays_list);

        /*
         *        * ------------------------------------ *
         *  ----- | STOP DOING STUFF WITH PARTICLE IMAGE | ----------------------------------------------------  ||  ---
         *        * ------------------------------------ *
         */



        *particle_counter += 1;

        // free memory of particle array
        free(particle_array);

        /*
        +1 for the trailer boundary slice. Grayscale data has two, but
        just one is included in the slice counter of the particle header.
        */
        i += particle_slices+1;
    }
    free(bit_array);
}





/*
 *      * ----------------------------------------------- *
 * ---  | Python wrapper for decompressing OAP imagefiles | ------------------------------------------------------------
 *      * ----------------------------------------------- *
 */
static PyObject *
decompress(PyObject *module, PyObject *args, PyObject *kwargs)
{
    // Record time for runtime measurement.
    clock_t start = clock();

    // --- Keyword arguments -------------------------------------------------------------------------------------------
    const char *filename;
    PyObject *timeframes = Py_None;
    PyObject *x_sizes = Py_None;
    PyObject *y_sizes = Py_None;
    PyObject *arrays_list = Py_None;
    PyObject *exclude_buffers = Py_None;
    PyObject *include_buffers = Py_None;
    int truncated = 0;
    int poisson = 0;
    int cluster = 0;
    int principal = 0;
    int status = 0;
    int buffer_id = 0;

    static char *kwlist[] = {"filename",
                             "timeframes",
                             "x_sizes",
                             "y_sizes",
                             "arrays",
                             "exclude_buffers",
                             "include_buffers",
                             "truncated",
                             "poisson",
                             "cluster",
                             "principal",
                             "status",
                             "buffer_id",
                             NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|OOOOOOpppppp", kwlist,
                                     &filename,
                                     &timeframes,
                                     &x_sizes,
                                     &y_sizes,
                                     &arrays_list,
                                     &exclude_buffers,
                                     &include_buffers,
                                     &truncated,
                                     &poisson,
                                     &cluster,
                                     &principal,
                                     &status,
                                     &buffer_id))
        Py_RETURN_NONE;

    FILE *imagefile = fopen(filename, "rb");

    if (imagefile == NULL)
    {
        Py_RETURN_NONE;     // ToDo: missing error handling!
    }

    /*
    Count the number of bytes in the imagefile.
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
    unsigned int n_buffers = file_bytes / 4112;
    unsigned char header[16];
    unsigned char buffer[4096];

    /*
    Number of imagefile particles, biterrors in the particle header,
    zero pixel images and truncated particle images.
    */
    unsigned int particle_counter = 0;
    unsigned int biterror_counter = 0;
    unsigned int zropxels_counter = 0;
    unsigned int trncated_counter = 0;

    for(unsigned int i=0; i<=n_buffers; i++)    // ToDo: last buffer?
    {
        fread(header, 1, 16, imagefile);
        fread(buffer, 1, 4096, imagefile);

        // --- Print Status Report -------------------------------------------------------------------------------------
        if (status)
        {
            if (i == 0)
            {
                // Bytes in the header are swapped.
                int year = (header[1] << 8 | header[0]);
                int month = (header[3] << 8 | header[2]);
                int day = (header[5] << 8 | header[4]);

                printf("\n--- Status Report ---\n\n");
                printf("File was recorded on %s %d, %d\n\n", MONTH[month-1], day, year);
                printf("Size (B): %ld\n", file_bytes);
                printf("# Buffer: %ld\n\n", n_buffers);
            }
            if (buffer_id)
            {
                printf("\rBuffer ID: %d", i);
                if (i == n_buffers)
                    printf("\n");
            }
            else
                progress_bar(i, n_buffers, 20, "Analyse ", " Complete");
        }

        // Explicitly exclude buffers or analyze only specific buffers.
        if (exclude_buffers != Py_None)
        {
            if (check_if_value_is_in_list(i, exclude_buffers))
                continue;
        }
        if (! check_if_value_is_in_list(i, include_buffers))
            continue;

        decompress_grayscale_buffer(buffer,
                                    &particle_counter,
                                    &biterror_counter,
                                    &zropxels_counter,
                                    &trncated_counter,
                                    timeframes,
                                    x_sizes,
                                    y_sizes,
                                    truncated,
                                    poisson,
                                    cluster,
                                    principal,
                                    arrays_list);
    }
    fclose(imagefile);

    // --- Print Status Report -----------------------------------------------------------------------------------------
    if (status)
    {
        printf("\nParticles: %d\n", particle_counter);
        printf("Truncated: %d\n", trncated_counter);
        printf("Biterrors: %d buffers affected\n", biterror_counter);
        printf("Zero Pxls: %d particle images\n", zropxels_counter);
        printf("\nRuntime %Lfs\n\n", (long double)(clock() - start)  / CLOCKS_PER_SEC);
    }

    // set reference count to zero
    Py_DECREF(timeframes);
    Py_DECREF(x_sizes);
    Py_DECREF(y_sizes);
    Py_DECREF(exclude_buffers);
    Py_DECREF(include_buffers);

    return PyLong_FromLong(particle_counter);
}
