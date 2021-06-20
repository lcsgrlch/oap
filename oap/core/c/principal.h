/*
Calculates the principal components of the particle array.
*/



double
mse(unsigned char *array_a, unsigned char *array_b, int array_length)
{
    double error;
    for (int i=0; i<array_length; i++)
    {
        error += (array_a[i] - array_b[i]) * (array_a[i] - array_b[i]);
    }
    error /= array_length;
    return error;
}



void
principal_components(unsigned char *array,
                     int img_height,
                     double *hit_ratio,
                     double *alpha_value,
                     double *axis_ratio,
                     double *mse_ellipse)
{
    double sum_x = 0.0;
    double sum_y = 0.0;
    double sum_xx = 0.0;
    double sum_yy = 0.0;
    double sum_xy = 0.0;
    double number_pix = 0.0;

    for (int y=0; y<img_height; y++)
    {
        for (int x=0; x<64; x++)
        {
            if (array[y*64+x] != 0)
            {
                sum_x += x;
                sum_y += y;
                sum_xx += x*x;
                sum_yy += y*y;
                sum_xy += x*y;
                number_pix += 1;
            }
        }
    }

    if (number_pix == 0)
        return;

    double x_bary = sum_x / number_pix;
    double y_bary = sum_y / number_pix;

    // Calculating the variance and the covariance.
    double var_x = sum_xx / number_pix - x_bary * x_bary;
    double var_y = sum_yy / number_pix - y_bary * y_bary;
    double cov_xy = sum_xy / number_pix - x_bary * y_bary;

    double discriminant = (var_x - var_y) * (var_x - var_y) + 4 * cov_xy * cov_xy;
    double sqrt_discr = sqrt(discriminant);

    double lambda_plus = ((var_x + var_y) + sqrt_discr) / 2.0;
    double lambda_minus = ((var_x + var_y) - sqrt_discr) / 2.0;

    // --- Eigenvectors ---
    double x_plus = var_x + cov_xy - lambda_minus;
    double y_plus = var_y + cov_xy - lambda_minus;
    double x_minus = var_x + cov_xy - lambda_plus;
    double y_minus = var_y + cov_xy - lambda_plus;

    // Normalizing the vectors.
    double denom_plus = sqrt(x_plus * x_plus + y_plus * y_plus);
    double denom_minus = sqrt(x_minus * x_minus + y_minus * y_minus);

    // Computing the normalized vector, which is parallel to the
    // longest axis of a particle image.
    double x_parallel;
    double y_parallel;
    if (denom_plus != 0)
    {
        x_parallel = x_plus / denom_plus;
        y_parallel = y_plus / denom_plus;
    }
    else
    {
        x_parallel = x_plus;
        y_parallel = y_plus;
    }

    // Computing the normalized vector, which is corresponding the
    // Normal of a particle image.
    double x_normal;
    double y_normal;
    if (denom_minus == 0)
    {
        x_normal = x_minus / denom_minus;
        y_normal = y_minus / denom_minus;
    }
    else
    {
        x_normal = x_minus;
        y_normal = y_minus;
    }

    if (lambda_plus < 0)
        lambda_plus = 0;
    if (lambda_minus < 0)
        lambda_minus = 0;

    double major_axis = 2 * sqrt(lambda_plus);
    double minor_axis = 2 * sqrt(lambda_minus);

    // Computing the rotation of the principal components.
    double alpha = 90 * (M_PI/180) ;   // 90 degrees in radians! ~ 1.5708
    if (x_parallel != 0)
        alpha = atan(y_parallel / x_parallel);

    double cos_alpha = cos(alpha);
    double sin_alpha = sin(alpha);

    if (minor_axis == 0)
        minor_axis = 0.0000001;
    if (major_axis == 0)
        major_axis = 0.0000001;

    double b = minor_axis * minor_axis;
    double a = major_axis * major_axis;

    int polygon_hits = 0;
    int ellipse_hits = 0;
    int polygon_misses = 0;
    int ellipse_misses = 0;

    unsigned char *ellipse_array;
    ellipse_array = (unsigned char*) calloc(img_height*64, sizeof(unsigned char));
    unsigned char *one_color_array;
    one_color_array = (unsigned char*) calloc(img_height*64, sizeof(unsigned char));

    bool intersect_ellipse;
    double denom_x;
    double denom_y;

    for (int y=0; y<img_height; y++)
    {
        for (int x=0; x<64; x++)
        {
            denom_x = cos_alpha * (x - x_bary) + sin_alpha * (y - y_bary);
            denom_y = sin_alpha * (x - x_bary) - cos_alpha * (y - y_bary);

            if (((denom_x * denom_x) / a) + ((denom_y * denom_y) / b) <= 1)
                intersect_ellipse = true;
            else
                intersect_ellipse = false;

            if (intersect_ellipse == true && array[y*64+x] != 0)
                ellipse_hits += 1;
            else if (array[y*64+x] != 0)
                ellipse_misses += 1;
            else if (intersect_ellipse == true && array[y*64+x] == 0)
                ellipse_misses += 1;

            if (mse_ellipse != NULL)
            {
                if (intersect_ellipse == true)
                    ellipse_array[y*64+x] = 1;
                if (array[y*64+x] != 0)
                    one_color_array[y*64+x] = 1;
            }
        }
    }

    *hit_ratio = (ellipse_hits / (double) (ellipse_misses + ellipse_hits));
    *alpha_value = alpha * (180.0/M_PI);  // Convert radian to degree.
    *axis_ratio = major_axis / minor_axis;

    if (mse_ellipse != NULL)
        *mse_ellipse = mse(one_color_array, ellipse_array, img_height*64);

    free(ellipse_array);
    free(one_color_array);
}
