#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

void get_name(int i, char name[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage ./recover [file]\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open the file, exiting\n");
        return 1;
    }

    FILE *output = fopen("trash.txt", "w"); // just having something open, so i can close successfully later
    if (output == NULL)
    {
        printf("Could not open the file, exiting\n");
        return 1;
    }

    uint8_t buffer[512];

    // apro il file e scrivo finché non accade di nuovo
    // se accade di nuovo chiudo il file, apro una ltro e scrivo ancora
    // così via fino alla fine di input.
    int i = 0;
    while (fread(buffer, sizeof(uint8_t), 512, input))
    {

        // i have new buffer, so i close last one and create new one
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] >= 0xe0 && buffer[3] <= 0xef))
        {
            // closing the shit if i find it
            fclose(output);

            // gettting file name
            char name[8];
            get_name(i, name);

            printf("%s  il valore di i è %d \n", name, i);
            output = fopen(name, "w");
            if (output == NULL)
            {
                printf("Could not open the file, exiting\n");
                return 1;
            }
            i++; // per il nome
        }

        fwrite(buffer, sizeof(uint8_t), 512, output);

    }

    fclose(output);
    fclose(input);

    // if true, i fouind a jpeg

}

void get_name(int i, char name[])
{
    char *temp = "000.jpg";
    char tmp[] = {(i / 100) % 10 + 0x30, (i / 10) % 10 + 0x30, i % 10 + 0x30};
    for (int j = 0; j < 3; j++)
    {
        name[j] = tmp[j];
    }
    for (int j = 3; j < 8; j++)
    {
        name[j] = temp[j];
    }
    return;
}