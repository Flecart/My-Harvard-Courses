// Implements a dictionary's functionality

#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 2099191;
// const unsigned int N = 1e9 + 9;

// Number of words;
int number_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int hash_value = hash(word);
    // in teoria questa linea è inutile...
    // dovrebbe già farlo dentro, ma non lo so...
    hash_value %= N;

    // probably i got some ' in high positions'
    if (hash_value < 0)
    {
        return false;
    }
    for (node *tmp = table[hash_value]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
    }

    // todo risolvere il problema di creare linked lists se lhash è già preso.

    return false;
}

// Hashes word to a number
// adapted from https://www.geeksforgeeks.org/string-hashing-using-polynomial-rolling-hash-function/
unsigned int hash(const char *word)
{
    // normalizing word;
    char copy[LENGTH + 1];
    strcpy(copy, word);
    for (int i = 0, len = strlen(copy); i < len; i++)
    {
        copy[i] = tolower(copy[i]);
    }

    // P and M
    int p = 31;
    unsigned int m = N;
    long long power_of_p = 1;
    long long hash_val = 0;

    // Loop to calculate the hash value
    // by iterating over the elements of string
    for (int i = 0; i < strlen(copy); i++)
    {
        hash_val = (hash_val + (copy[i] - 'a' + 1) * power_of_p) % m;
        power_of_p = (power_of_p * p) % m;
    }
    return hash_val;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // initialize every entry of table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // opening the file
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }

    node *tmp = malloc(sizeof(node));
    if (tmp == NULL)
    {
        return false;
    }
    tmp->next = NULL;

    int index = 0;
    // beginning to read from the dictionary
    char c;
    while (fread(&c, sizeof(char), 1, input))
    {
        if (c != '\n')
        {
            tmp->word[index] = c;
            index++;
        }

        // end of a word,
        else
        {
            //terminating the string
            tmp->word[index] = '\0';


            // allocating it into memory, by calculating the hash first
            unsigned int hash_value = hash(tmp->word);
            hash_value %= N;
            // if (hash_value == 129674)
            // {
            //     printf("%s", tmp->word);
            //     return false;
            // } ## idioms same hash of recognized, check cant get this shit fuk

            // if its free, then point to the current word
            if (table[hash_value] == NULL)
            {
                table[hash_value] = tmp;
            }
            // else go to next possible position
            else
            {
                node *i = table[hash_value];
                table[hash_value] = tmp;
                table[hash_value]->next = i;
            }

            // reset values
            index = 0;
            tmp = malloc(sizeof(node));
            if (tmp == NULL)
            {
                unload();
                return false;
            }
            tmp->next = NULL;

            number_words++;
        }
    }

    // at the end of the cycle tmp has a garbage value
    // because it allocates in last loop, which has no good chars.
    free(tmp);
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return number_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // adaptation from notes;
        node *list = table[i];
        while (list != NULL)
        {
            // We point to the next node first
            node *tmp = list->next;
            // Then, we can free the first node
            free(list);
            // Now we can set the list to point to the next node
            list = tmp;
            // If list is null, when there are no nodes left, our while loop will stop
        }
    }
    return true;
}
