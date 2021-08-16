#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
void encrypt(string plaintext, int key);
int convert_int(string number);


int main(int argc, string argv[])
{
    // handles the argc
    if (argc != 2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }

    int key = convert_int(argv[1]);
    if (key == -1)
    {
        printf("Usage: ./caesar key");
        return 1;
    }

    //ciphering
    string plaintext = get_string("plaintext: ");
    string ciphertext = plaintext;
    encrypt(ciphertext, key);
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}

// the input i got is a string, and this is a problem
int convert_int(string number)
{
    int len = strlen(number), ans = 0;
    for (int i = 0; i < len; i++)
    {
        // checking the range, from 0 to 9
        int is_number = number[i] - 0x30; // -x30 is ascci for numbers

        // exit if not a number
        if (is_number > 9 || is_number < 0)
        {
            return -1;
        }

        // creating the number
        ans += pow(10, len - i - 1) * (is_number);
    }
    return ans;
}

// differenzio nel caso sia maiuscolo o minuscolo
void encrypt(string plaintext, int key)
{
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        if (isupper(plaintext[i]))
        {
            plaintext[i] -= 0x41;
            plaintext[i] = (plaintext[i] + key) % 26;
            plaintext[i] += 0x41;
        }
        else if (islower(plaintext[i]))
        {
            plaintext[i] -= 0x61;
            plaintext[i] = (plaintext[i] + key) % 26;
            plaintext[i] += 0x61;
        }
    }
}