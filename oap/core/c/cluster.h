/*
Very simple algorithm to detect whether a particle image contains
multiple particle clusters respectively multiple particles.
*/



void
flood_fill(unsigned char *array, int x, int y, int y_dim, int x_min, int x_max, int marker)
{
    if (x >= x_min && x <= x_max && y >= 0 && y < y_dim)
    {
        if (array[y*64+x] == 1 || array[y*64+x] == 2 || array[y*64+x] == 3)
        {
            array[y*64+x] = marker;
            flood_fill(array, x, y+1, y_dim, x_min, x_max, marker);
            flood_fill(array, x, y-1, y_dim, x_min, x_max, marker);
            flood_fill(array, x+1, y, y_dim, x_min, x_max, marker);
            flood_fill(array, x-1, y, y_dim, x_min, x_max, marker);
            flood_fill(array, x+1, y+1, y_dim, x_min, x_max, marker);
            flood_fill(array, x-1, y-1, y_dim, x_min, x_max, marker);
            flood_fill(array, x+1, y-1, y_dim, x_min, x_max, marker);
            flood_fill(array, x-1, y+1, y_dim, x_min, x_max, marker);
        }
    }
    return;
}



int
particle_cluster(unsigned char *array, int y_dim, int x_min, int x_max)
{
    int marker = 10;
    for (int y=0; y<y_dim; y++)
    {
        for (int x=x_min; x<=x_max; x++)
        {
            if (array[y*64+x] == 1 || array[y*64+x] == 2 || array[y*64+x] == 3)
            {
                flood_fill(array, x, y, y_dim, x_min, x_max, marker);
                marker += 1;
            }
        }
    }
    return (marker - 10);
}
