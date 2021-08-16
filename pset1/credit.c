#include <cs50.h>
#include <stdio.h>

int verify(long n);

long myPow(int x, int n);

long get_rid_zeros(long n);

int get_len(long n);

void final_output(long n);

long get_last_two(long n, int len);

int main(void)
{
    // getting th efirst input
    long n = get_long("Input credit card: ");

    // verifying checksum
    int is_valid = verify(n);

    if (is_valid == 0)
    {
        printf("INVALID\n");
        return 0;
    }
    else
    {
        final_output(n);
        return 0;
    }
}

long myPow(int x, int n)
{
    int i; /* Variable used in loop counter */
    long number = 1;

    for (i = 0; i < n; ++i)
    {
        number *= x;
    }
    return (number);
}

int verify(long n)
{
    // getting len of the number
    int check = 0, i, final;


    // correct last ++ who made the number bigger
    // noo i dont need to correct last + because there is the number 1...

    i = 2;
    while (myPow(10, i) < n * 10)
    {
        // this code sucks, i should make a function, but im so noob.
        // ma prende le posizioni e fa le operazioni che deve fare come da algoritmo
        long temp = get_rid_zeros(((n % myPow(10, i)) - (n % myPow(10, i - 1)))) * 2;

        if (temp < 10)
        {
            check += temp;
        }
        else
        {
            check += (temp % 10) + ((temp - temp % 10) / 10);
        }

        i += 2;
    }

    // reusing the variable for the second sum
    i = 1;
    while (myPow(10, i) < n * 10)
    {
        check += get_rid_zeros(((n % myPow(10, i)) - (n % myPow(10, i - 1))));
        i += 2;
    }

    // checking the last number in this way
    final = check % 10;

    if (final == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

// gives all the zeros a shit, li butta via lel
long get_rid_zeros(long n)
{
    if (n == 0)
    {
        return 0;
    }
    while (n % 10 == 0)
    {
        n /= 10;
    }
    return n;
}

// gets the len of the number, i dunno if it always works
int get_len(long n)
{
    int len = 0;
    while (myPow(10, len) < n)
    {
        len++;
    }
    return len;
}

// gets the last two of a number.
long get_last_two(long n, int len)
{
    long ans;

    ans = n - (n % myPow(10, len - 2));
    ans = get_rid_zeros(ans);
    if (ans < 10)
    {
        ans *= 10;
    }
    return ans;
}

// this code checks for the parameters of the exercise,  just a lot of if conditions
void final_output(long n)
{
    int len = get_len(n);


    // ALMOST SURE ITS AMERICAN EXPRESS, JUST CHECK THE START
    if (len == 15)
    {
        int last_two = get_last_two(n, len);
        if ((last_two == 34) || (last_two == 37))
        {
            printf("AMEX");
        }
        else
        {
            printf("INVALID");
        }
    }

    // ALMOST SURE ITS VISA, JUST CHECK THE START
    else if (len == 13)
    {
        int last_two = get_last_two(n, len);
        last_two /= 10;
        if (last_two == 4)
        {
            printf("VISA");
        }
        else
        {
            printf("INVALID");
        }

    }

    // IF ITS LONG 16 WE CAN DO MORE THINGS!
    else if (len == 16)
    {
        int last_two = get_last_two(n, len);
        int visa_check = last_two / 10;
        if (visa_check == 4)
        {
            printf("VISA");
        }
        else if ((last_two == 51) || (last_two == 52) || (last_two == 53) || (last_two == 54) || (last_two == 55))
        {
            printf("MASTERCARD");
        }
        else
        {
            printf("INVALID");
        }
    }
    else
    {
        printf("INVALID");
    }
    printf("\n");
}