#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// function for letters per words
float get_L(string text);

// function for sentences / words.
float get_S(string text);

int main(void)
{
    string text = get_string("Text: ");

    float L = get_L(text);
    float S = get_S(text);

    // i need this to be a float... wtf of a bug
    float grade = 0.0588 * L - 0.296 * S - 15.8;


    int compare;

    // rounding the number to compare with
    if (grade - (int) grade >= 0.5)
    {
        compare = (int) grade + 1;
    }
    else
    {
        compare = (int) grade;
    }


    // now i have to make cases... nothing fancy
    if (compare > 16)
    {
        printf("Grade 16+\n");
    }
    else if (compare < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", compare);
    }
}

float get_L(string text)
{
    int letters = 0, words = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // count the words, i dont want to count empty as word, like -! -
        // i don't want to begin to count from 0
        // and strangely you're are not 2 words...
        if ((!isalpha(text[i])) && isalpha(text[i - 1]) && i > 0 && text[i] != '\'' && text[i] != '-')
        {
            words++;
        }
        else if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return (float) letters / words * 100;
}

float get_S(string text)
{
    int words = 0, sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // count the words, i dont want to count empty as word, like -! -
        if ((!isalpha(text[i])) && isalpha(text[i - 1]) && i > 0 && text[i] != '\'' && text[i] != '-')
        {
            words++;
            if ((text[i] == '!' || text[i] == '.' || text[i] == '?') && isalpha(text[i - 1]))
            {
                sentences++;
            }
        }
    }

    return (float) sentences / words * 100;
}