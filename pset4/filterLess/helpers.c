#include "helpers.h"
#include <math.h>
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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE red, green, blue;
            int tempRed, tempGreen, tempBlue;
            red = image[i][j].rgbtRed;
            green = image[i][j].rgbtGreen;
            blue = image[i][j].rgbtBlue;

            tempRed = (int) round(.393 * red + .769 * green + .189 * blue);
            tempGreen = (int) round(.349 * red + .686 * green + .168 * blue);
            tempBlue = (int) round(.272 * red + .534 * green + .131 * blue);

            if (tempRed > 255)
            {
                tempRed = 255;
            }
            if (tempGreen > 255)
            {
                tempGreen = 255;
            }
            if (tempBlue > 255)
            {
                tempBlue = 255;
            }
            image[i][j].rgbtRed = tempRed;
            image[i][j].rgbtGreen = tempGreen;
            image[i][j].rgbtBlue = tempBlue;
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
