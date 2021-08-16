#include "helpers.h"
#include <math.h>
// need this to control the value in edge
BYTE cap_int(int colorValue)
{
    if (colorValue > 255)
    {
        colorValue = 255;
    }
    return colorValue;
}
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate mean of current pixel and update pixel value;
            float mean = (image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0;
            mean  = round(mean);
            image[i][j].rgbtBlue = (int) mean;
            image[i][j].rgbtRed = (int) mean;
            image[i][j].rgbtGreen = (int) mean;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image

// algoritmo schifoso da debuggare
// dovevi creare dei box e poi fare loop sui box e non hardcodare tutto!
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // using this to store eveything
    RGBTRIPLE temp[height][width];
    // looping through all pixels of the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // setting variables to count and making the mean
            int red = 0, green = 0, blue = 0;
            float count = 0.0; // how many pixels ive been counting
            for (int u = i - 1; u <= i + 1; u++)
            {
                // checking boundaries
                if (u < 0 || u >= height)
                {
                    continue;
                }

                for (int k = j - 1; k <= j + 1; k++)
                {
                    if (k < 0 || k >= width)
                    {
                        continue;
                    }

                    // counting up the values
                    red += image[u][k].rgbtRed;
                    blue += image[u][k].rgbtBlue;
                    green += image[u][k].rgbtGreen;
                    count++;
                }
            }

            temp[i][j].rgbtRed = (int) round(red / count);
            temp[i][j].rgbtBlue = (int) round(blue / count);
            temp[i][j].rgbtGreen = (int) round(green / count);
        }
    }

    // copyng everything back to image

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // using this to store eveything
    RGBTRIPLE temp[height][width];
    // looping through all pixels of the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // setting variables to count and making the mean
            int red = 0, green = 0, blue = 0; // these will store the x value
            int red2 = 0, green2 = 0, blue2 = 0; // store the y value

            short gx[][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            short gy[][3] = {{1, 0, -1}, {2, 0, -2}, {1, 0, -1}};

            for (int u = i - 1; u <= i + 1; u++)
            {
                // checking boundaries
                if (u < 0 || u >= height)
                {
                    // i valori dei pixel aumentano di 0;
                    continue;
                }

                for (int k = j - 1; k <= j + 1; k++)
                {
                    if (k < 0 || k >= width)
                    {
                        // i valori dei pixel aumentano di 0;
                        continue;
                    }

                    // counting up the values
                    int i_offset = u - i + 1, j_offset = k - j + 1;

                    red += image[u][k].rgbtRed * gx[i_offset][j_offset];
                    blue += image[u][k].rgbtBlue * gx[i_offset][j_offset];
                    green += image[u][k].rgbtGreen * gx[i_offset][j_offset];
                    red2 += image[u][k].rgbtRed * gy[i_offset][j_offset];
                    blue2 += image[u][k].rgbtBlue * gy[i_offset][j_offset];
                    green2 += image[u][k].rgbtGreen * gy[i_offset][j_offset];
                }
            }
            red = (int) round(sqrt((double)(red * red + red2 * red2)));
            blue = (int) round(sqrt((double)(blue * blue + blue2 * blue2)));
            green = (int) round(sqrt((double)(green * green + green2 * green2)));
            temp[i][j].rgbtRed = cap_int(red);
            temp[i][j].rgbtBlue = cap_int(blue);
            temp[i][j].rgbtGreen = cap_int(green);
        }
    }
    // copyng everything back to image

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

