#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

void reset_verified(bool visited[]);
bool isCyclicUtil(int candidate, bool visited[], bool recStack[]);
bool isCyclic(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            // i stora la posizione del candidato (quindi il nome)
            // rank stora il valore del candidato.
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // - 1 perché tanto l'ultimo non vince con nessuno, e non vado in overflow
    for (int i = 0; i < candidate_count - 1; i++)
    {
        // ranks[i] è il vincitore del momento
        // ranks[j] nell'altro ciclo è chi sta perdendo contro i;
        // questo solamente nel singolo voto di una persona.

        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // variabile temporanea che mi serve per aggiornare pairs
            pair temp;

            // check quale dei due è maggiore dell'altro
            // e creo il pair
            if (preferences[i][j] > preferences[j][i])
            {
                temp.winner = i;
                temp.loser = j;

                // aggirono pairs con il valore di temp creato prima
                pairs[pair_count] = temp;
                pair_count++;
            }
            // questo else comprende anche il caso uguale
            // potrebbe dare dei bug, ma intanto lo metto su.
            else if (preferences[i][j] < preferences[j][i])
            {
                temp.winner = j;
                temp.loser = i;

                // aggirono pairs con il valore di temp creato prima
                pairs[pair_count] = temp;
                pair_count++;
            }

            else
            {
                // if equal do nothing
            }


        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    bool swapped = true;
    while (swapped)
    {
        swapped = false;
        // per essere un pò più efficiente dovrei fare meno swap finali
        // ma dovrei creare una altra variabile? no, non va
        for (int i = 0; i < pair_count - 1; i++)
        {
            pair first = pairs[i], second = pairs[i + 1];

            if (preferences[first.winner][first.loser] < preferences[second.winner][second.loser])
            {
                // swapping
                swapped = true;
                pairs[i + 1] = first;
                pairs[i] = second;

            }
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{

    for (int i = 0; i < pair_count; i++)
    {
        locked[pairs[i].winner][pairs[i].loser] = true;

        // se creando questo collegamento trovo un ciclo, mi stoppo e vado oltre
        if (isCyclic())
        {
            locked[pairs[i].winner][pairs[i].loser] = false;
        }
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{

    for (int i = 0; i < candidate_count; i++)
    {
        // se nessuno punta a questo vuol dire che sia l'origine
        // questa variabile stora questa informazione
        bool arrow_to_me = false;
        for (int j = 0; j < candidate_count; j++)
        {
            // se esiste una freccia che mi punta, vuol dire che non è origine
            if (locked[j][i])
            {
                arrow_to_me = true;
                break;
            }
        }
        if (!arrow_to_me)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
    return;
}

bool isCyclicUtil(int candidate, bool visited[], bool recStack[])
{
    visited[candidate] = true;
    recStack[candidate] = true;
    for (int i = 0; i < candidate_count; i++)
    {
        // se ce un collegamento continua a cercare lì
        if (locked[candidate][i])
        {
            if (!visited[i] && isCyclicUtil(i, visited, recStack))
            {
                // se questo è vero, vuol dire che sta andando
                // in un punto in cui è già stato
                // quindi è ciclico
                return true;
            }
            else if (recStack[i])
            {
                return true;
            }

            // se è già visitato allora crea il ciclo omg!
            // return true;

        }
    }
    recStack[candidate] = false;
    // se non ce niente di quelli prima ritorna falso
    return false;
}

bool isCyclic(void)
{
    bool visited[candidate_count], recStack[candidate_count];
    reset_verified(visited);
    reset_verified(recStack);


    // non voglio iniziare a guardare uno che sia già stato visto, tanto lo ho già visto!
    // int i = pairs[0].winner;
    for (int i = 0; i < candidate_count; i++)
    {
        if (!visited[i])
        {
            // -1 per dire che è il padre, vertice primo da cui inizio.
            if (isCyclicUtil(i, visited, recStack))
            {
                return true;
            }
        }
    }


    // se per tutto prima non trova niente falsooo
    return false;


}

void reset_verified(bool visited[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        visited[i] = false;
    }
    return;
}