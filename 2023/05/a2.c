// this was not a good idea
// it segfaults if there isn't a trailing newline in the input lol

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    FILE *file = fopen("05/input", "r");

    fseek(file, 0, SEEK_END);
    long fileLength = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *data = malloc(fileLength+1);
    data[fileLength] = 0;

    fread(data, sizeof(char), fileLength, file);
    fclose(file);

    char *curr = data;

    unsigned seeds[32] = {0};
    unsigned seedCount = 0;

    {
        bool processingNumber = false;
        char c;

        do {
            c = *curr++;

            if ('0' <= c && c <= '9') {
                seeds[seedCount] = seeds[seedCount]*10 + c-48;
                processingNumber = true;
            } else if (processingNumber) {
                seedCount++;
                processingNumber = false;
            }
        } while (c != '\n');
    }

    unsigned maps[7][64][3] = {0};
    unsigned mapSizes[7] = {0};
    for (unsigned i=0; i < 7; ++i) {
        curr = strchr(curr+1, '\n') + 1;

        while (*curr != '\n' && *curr != 0) {
            sscanf(curr, "%u %u %u", maps[i][mapSizes[i]] + 0, maps[i][mapSizes[i]] + 1, maps[i][mapSizes[i]] + 2);
            mapSizes[i]++;
            curr = strchr(curr, '\n') + 1;
        }
    }

    for (unsigned locationNumber=0;; ++locationNumber) {
        unsigned x = locationNumber;
        for (int i=6; i >= 0; --i) {
            for (unsigned j=0; j < mapSizes[i]; ++j) {
                if (maps[i][j][0] <= x && x < maps[i][j][0] + maps[i][j][2]) {
                    x = maps[i][j][1] + x - maps[i][j][0];

                    break;
                }
            }
        }

        for (unsigned i=0; i < seedCount; i += 2) {
            if (seeds[i] <= x && x < seeds[i] + seeds[i+1]) {
                printf("%u\n", locationNumber);
                goto END;
            }
        }
    }

    END:

    free(data);
}
