#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

bool is_valid_cipher(string cipher);

int cmpfunc(const void *a, const void *b);

void cipher_this(string plaintext, string cipher);

char encrypt(char ch, string cipher);


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("You need to input one argument!");
        return 1;
    }
    else if (!is_valid_cipher(argv[1]))
    {
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = plaintext; // put pointers, so its clearer
    cipher_this(ciphertext, argv[1]);


    printf("ciphertext: %s\n", ciphertext);
}

// unknown stuff for sorting
int cmpfunc(const void *a, const void *b)
{
    return *(char *)a - *(char *)b;
}

primo reversed
secondo sorted
terzo random

in ordine sono 1,2,3

real    0m13.283s
user    0m4.619s
sys     0m0.064s
real    0m3.707s
user    0m0.023s
sys     0m0.076s
real    0m16.166s
user    0m6.290s
sys     0m0.080s
__
real    0m5.654s
user    0m0.038s
sys     0m0.101s
real    0m2.822s
user    0m0.036s
sys     0m0.073s
real    0m3.700s
user    0m0.032s
sys     0m0.085s
___
real    0m7.557s
user    0m2.476s
sys     0m0.072s
real    0m9.749s
user    0m2.547s
sys     0m0.076s
real    0m9.547s
user    0m2.390s
sys     0m0.089s
// just want to check if the substitution cipher is correct, if yes continue the main program
bool is_valid_cipher(string cipher)
{
    if (strlen(cipher) != 26)
    {
        printf("Your cipher does not contain 26 characters!");
        return false;
    }
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(cipher[i]))
        {
            printf("Your cipher contains illegal characters!");
            return false;
        }
        // i want to standardize the input to only uppercase chars!
        else if (islower(cipher[i]))
        {
            cipher[i] -= 32;
        }
    }

    // later i have to sort the cipher, but i dont want to change it
    // so i have to create new array
    char copy_for_comparison[27];
    strncpy(copy_for_comparison, cipher, 27);

    // so its easier to compare
    // it shouldnt hcange cipher so i use new variable
    qsort(copy_for_comparison, 26, sizeof(char), cmpfunc);

    for (int i = 'A'; i <= 'Z'; i++)
    {
        if ((int) copy_for_comparison[i - 'A'] != i)
        {
            printf("Your cipher contains multiple characters!");
            return false;
        }
    }
    return true;
}

void cipher_this(string plaintext, string cipher)
{
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        plaintext[i] = encrypt(plaintext[i], cipher);
    }
}

// just getting the index of the char, so i can use substitution
// like A is 0, as a, B is 1 and so on
char encrypt(char ch, string cipher)
{
    if (isupper(ch))
    {
        int index =  ch - 'A';
        ch = cipher[index];
    }
    else if (islower(ch))
    {
        int index = ch - 'a';
        ch = cipher[index] + 0x20; // so i get lower character instead of upper
    }
    else
    {
        // DO NOTHING, BC it might be a space or comma.
    }
    return ch;
}