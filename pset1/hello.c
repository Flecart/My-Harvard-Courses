#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get and print the name
    string name = get_string("What is your name?\n");
    printf("Hello, %s", name);
}