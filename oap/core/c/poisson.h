/*
Poisson spot labeling and evaluation.
*/

const unsigned char POISSON_SPOT_MARKER = 7;



void
poisson_spot(unsigned char *array, int x, int y, int y_dim, int x_min, int x_max)
{
    /*
    Checks if the value for index (x,y) is zero. If true, the pixel
    gets marked with a PoissonSpot marker.
    */

    if (x >= x_min && x <= x_max && y >= 0 && y < y_dim)
    {
        if (array[y*64+x] == 0)
        {
            array[y*64+x] = POISSON_SPOT_MARKER;
            poisson_spot(array, x, y+1, y_dim, x_min, x_max);
            poisson_spot(array, x, y-1, y_dim, x_min, x_max);
            poisson_spot(array, x+1, y, y_dim, x_min, x_max);
            poisson_spot(array, x-1, y, y_dim, x_min, x_max);
        }
    }
    return;
}



void
evaluate_poisson_spot(unsigned char *array, int img_height, int min_index, int max_index, int *poisson_size)
{
    /*
    Measures the sizes of labeled Poisson Spots. If the Poisson Spot is not a closed
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
    for (int i=0; i<img_height; i++)
    {
        for (int j=0; j<64; j++)
        {
            if (array[i*64+j] == POISSON_SPOT_MARKER)
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
        if (array[x] == POISSON_SPOT_MARKER || array[(img_height-1)*64+x] == POISSON_SPOT_MARKER)
        {
            closed_circle = false;
        }
    }
    for (int y=0; y<img_height; y++)
    {
        if (array[y*64+min_index] == POISSON_SPOT_MARKER || array[y*64+max_index] == POISSON_SPOT_MARKER)
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

        for (int i=0; i<img_height; i++)
        {
            for (int j=0; j<64; j++)
            {
                if (array[i*64+j] == POISSON_SPOT_MARKER)
                {
                    array[i*64+j] = 0;
                }
            }
        }
    }
}
