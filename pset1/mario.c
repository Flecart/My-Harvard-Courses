#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get positive integer from user
    int n;
    do
    {
        n = get_int("Width: ");
    }
    while ((n < 1) || (n > 8));

    // I need these spaces, so i know how many to print
    // i want ti print N stuff per half line
    int spaces = n - 1;
    for (int i = 0; i < n; i++)
    {

        // in this first part i want to print the first half of piramid
        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }

        for (int j = spaces; j < n; j++)
        {
            printf("#");
        }

        // printing the two spaces
        printf("  ");


        // printing the second half of the piramid
        for (int j = spaces; j < n; j++)
        {
            printf("#");
        }

        // updating the spaces to print for the next move
        spaces--;

        // escape for new line, love it no?
        printf("\n");
    }

}