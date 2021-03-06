/*
Process the decompressed particle array.
All analyses and outputs of the particle image are defined here.
*/

void
process_particle_array(unsigned char *particle_array,
                       int slice_size,
                       int img_height,
                       int particle_width,
                       int particle_number,
                       int second_of_day,
                       int millisecond,
                       int microsecond,
                       int nanosecond,
                       int counter_1_pixels,
                       int counter_2_pixels,
                       int counter_3_pixels,
                       int number_of_pixels,
                       int min_index,
                       int max_index,
                       int x_bary,
                       int y_bary,
                       int particle_truncated,
                       int poisson,
                       int cluster,
                       int principal,
                       PyObject *arrays_list,
                       PyObject *images_list)
{

    // --- Poisson spot detection --------------------------------------------------------------------------------------

    // Size of the Poisson Spot -> Zero indicates there is either no spot
    // or no closed circle around the Poisson Spot.
    int poisson_size = 0;

    if (poisson && img_height >= 3 && particle_width >= 3 && number_of_pixels >= 4)
    {
        poisson_spot(particle_array, x_bary, y_bary, img_height, min_index, max_index);
        // Measure the Poisson Spot size and remove marker, if the circle
        // around the spot is not closed.
        evaluate_poisson_spot(particle_array, img_height, min_index, max_index, &poisson_size);
    }



    // --- Calculate principal components ------------------------------------------------------------------------------
    double hit_ratio = 0.0;
    double alpha_value = 0.0;
    double axis_ratio = 0.0;

    if (principal)
    {
        principal_components(particle_array, img_height, &hit_ratio, &alpha_value, &axis_ratio, NULL);
    }



    // --- Connected components (Cluser) -------------------------------------------------------------------------------
    int number_of_particle_cluster = 0;

    if (cluster)
    {
        // This algorithm colors the particle image therefore
        // a copy of the particle array must be made.
        unsigned char *particle_array_copy;
        particle_array_copy = (unsigned char*) malloc((img_height*slice_size) * sizeof(unsigned char));
        memcpy(particle_array_copy, particle_array, img_height*slice_size);
        number_of_particle_cluster = particle_cluster(particle_array_copy, img_height, min_index, max_index);
        free(particle_array_copy);
    }



    // --- Append particle image to list -------------------------------------------------------------------------------
    if (PyList_Check(images_list))
    {
        PyObject *particle_as_list = PyList_New(0);
        for (int y=0; y<img_height; y++)
        {
            for (int x=0; x<64; x++)
            {
                PyList_Append(particle_as_list, PyLong_FromLong(particle_array[y*64+x]));
            }
        }
        PyList_Append(images_list, particle_as_list);
        Py_DECREF(particle_as_list);
    }



    // --- Init OpticalArray -------------------------------------------------------------------------------------------
    if (PyList_Check(arrays_list))
    {
        OpticalArrayObject *optical_array;
        optical_array = (OpticalArrayObject *) OpticalArrayType.tp_alloc(&OpticalArrayType, 0);


        unsigned char *buffer;
        buffer = (unsigned char*) malloc((img_height*slice_size) * sizeof(unsigned char));
        memcpy(buffer, particle_array, img_height*slice_size);
        optical_array->array = buffer;
        // free(buffer);


        optical_array->second = second_of_day;
        optical_array->number = particle_number;
        optical_array->millisecond = millisecond;
        optical_array->microsecond = microsecond;
        optical_array->y_dim = img_height;
        optical_array->x_bary = x_bary;
        optical_array->y_bary = y_bary;
        optical_array->min_idx = min_index;
        optical_array->max_idx = max_index;
        optical_array->pixel_one = counter_1_pixels;
        optical_array->pixel_two = counter_2_pixels;
        optical_array->pixel_thr = counter_3_pixels;
        optical_array->poisson = poisson_size;
        //optical_array->poisson_mono = 0;
        optical_array->truncated = particle_truncated;
        optical_array->cluster = number_of_particle_cluster;
        optical_array->hit_ratio = hit_ratio;
        optical_array->axis_ratio = axis_ratio;
        optical_array->alpha = alpha_value;

        PyList_Append(arrays_list, (PyObject *) optical_array);
        Py_DECREF(optical_array);
    }
}
