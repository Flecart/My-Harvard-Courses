#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Just printing the winner maybe i should make a function, but im lazy to copy and paste
    // the prototype
    if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int ans = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        char ciao = word[i];

        // i have to know if its lower or upper character
        // then i substracht their offset :D
        if (islower(ciao))
        {
            ans += POINTS[ciao - 0x61];
        }
        else if (isupper(ciao))
        {
            ans += POINTS[ciao - 0x41];
        }
        else
        {
            // Do nothing because other values are 0;
        }


    }
    return ans;
}