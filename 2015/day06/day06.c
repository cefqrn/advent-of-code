#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

static void die(char *cause) {
    perror(cause);
    exit(1);
}

static void solve(char *input) {
    uint8_t  lights1[1000 * 1000] = {0};
    uint16_t lights2[1000 * 1000] = {0};

    char *r1 = NULL;
    for (char *c=strtok_r(input, "\n", &r1); c != NULL; c=strtok_r(NULL, "\n", &r1)) {
        char *r2 = NULL;
        char *command = strtok_r(c, " ", &r2);
        if (strcmp(command, "turn") == 0)  // ignore "turn"
            command = strtok_r(NULL, " ", &r2);

        int x1, y1, x2, y2;
        x1 = atoi(strtok_r(NULL, ",", &r2));
        y1 = atoi(strtok_r(NULL, " ", &r2));
        strtok_r(NULL, " ", &r2);  // ignore "through"
        x2 = atoi(strtok_r(NULL, ",", &r2));
        y2 = atoi(strtok_r(NULL, " ", &r2));

        switch (command[1]) {
        case 'n':  // on
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights1[x*1000 + y] = 1;
                    ++lights2[x*1000 + y];
                }
            }
            break;
        case 'f':  // off
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights1[x*1000 + y] = 0;
                    if (lights2[x*1000 + y])
                        --lights2[x*1000 + y];
                }
            }
            break;
        case 'o':  // toggle
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights1[x*1000 + y] ^= 1;
                    lights2[x*1000 + y] += 2;
                }
            }
        }
    }

    unsigned int p1 = 0, p2 = 0;
    for (size_t i=0; i < 1000000; ++i) {
        p1 += lights1[i];
        p2 += lights2[i];
    }

    printf("p1: %d\n", p1);
    printf("p2: %d\n", p2);
}

int main(int argc, char *argv[]) {
    FILE *fp;

    if (argc == 2) {
        fp = fopen(argv[1], "r");
        if (fp == NULL)
            die("fopen");
    } else if (!isatty(0)) {
        fp = stdin;
    } else {
        puts("input not given");
        exit(1);
    }

    fseek(fp, 0, SEEK_END);
    size_t len = ftell(fp);
    rewind(fp);
    
    char *input = calloc(len, sizeof *input);
    if (input == NULL)
        die("calloc");

    if (fread(input, sizeof(char), len, fp) == 0)
        die("fread");

    clock_t st = clock();
    solve(input);
    printf("done in %f s\n", (double)(clock() - st) / CLOCKS_PER_SEC);

    free(input);
    fclose(fp);
}