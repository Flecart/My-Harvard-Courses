#include <cs50.h>
#include <stdio.h>

int get_start_size(void);

int get_end_size(int n);

int calculate_time(int start, int end);

void print_answer(int ans);

// i want to first:
// get the population
// get the end population
// calculate the time with that formula
// at the end finish everything
int main(void)
{
    int start_size = get_start_size();
    int end_size = get_end_size(start_size);

    int ans = calculate_time(start_size, end_size);

    print_answer(ans);
}

// if i get a number under 9, population is stagnant
int get_start_size(void)
{
    int temp = get_int("Input the start size for the population: ");
    while (temp < 9)
    {
        temp = get_int("Input the start size for the population: ");
    }
    return temp;
}

// i dont want a number under the start size, it has no sense
int get_end_size(int n)
{
    int temp = get_int("Input the end size for the population: ");
    while (temp < n)
    {
        temp = get_int("Input the end size for the population: ");
    }
    return temp;
}

// calculates time with the rule he has told me
int calculate_time(int start, int end)
{
    int i = 0;
    while (start < end)
    {
        start += start / 3 - start / 4;
        i++;
    }
    return i;

}

void print_answer(int ans)
{
    printf("Years: %i", ans);
}