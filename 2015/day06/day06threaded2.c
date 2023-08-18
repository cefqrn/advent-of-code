#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#define COMMAND_ARRAY_SIZE 512

enum command_type {
    ON,
    OFF,
    TOGGLE
};

struct command {
    enum command_type type;
    size_t x1, y1, x2, y2;
};

struct thread_data {
    struct command commands[COMMAND_ARRAY_SIZE];
    size_t commandCount;
};

static void die(char *cause) {
    perror(cause);
    exit(1);
}

static void *p1t(void *args) {
    struct thread_data *data = args;
    struct command *commands = data->commands;

    uint8_t *lights = calloc(1000 * 1000, sizeof *lights);

    for (size_t i=0; i < data->commandCount; ++i) {
        size_t x1=commands[i].x1, y1=commands[i].y1, x2=commands[i].x2, y2=commands[i].y2;

        switch (commands[i].type) {
        case ON:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights[x*1000 + y] = 1;
                }
            }
            break;
        case OFF:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights[x*1000 + y] = 0;
                }
            }
            break;
        case TOGGLE:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights[x*1000 + y] ^= 1;
                }
            }
        }
    }

    unsigned int *result = calloc(1, sizeof *result);
    for (size_t i=0; i < 1000 * 1000; ++i) {
        *result += lights[i];
    }

    free(lights);

    return result;
}

static void *p2t(void *args) {
    struct thread_data *data = args;
    struct command *commands = data->commands;

    uint16_t *lights = calloc(1000 * 1000, sizeof *lights);

    for (size_t i=0; i < data->commandCount; ++i) {
        size_t x1=commands[i].x1, y1=commands[i].y1, x2=commands[i].x2, y2=commands[i].y2;

        switch (commands[i].type) {
        case ON:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    ++lights[x*1000 + y];
                }
            }
            break;
        case OFF:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    if (lights[x*1000 + y])
                        --lights[x*1000 + y];
                }
            }
            break;
        case TOGGLE:
            for (size_t x=x1; x <= x2; ++x) {
                for (size_t y=y1; y <= y2; ++y) {
                    lights[x*1000 + y] += 2;
                }
            }
        }
    }

    unsigned int *result = calloc(1, sizeof *result);
    for (size_t i=0; i < 1000 * 1000; ++i) {
        *result += lights[i];
    }

    free(lights);
    
    return result;
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

    struct thread_data data = {0};

    char *r1 = NULL;
    for (char *c=strtok_r(input, "\n", &r1); c != NULL; c=strtok_r(NULL, "\n", &r1)) {
        char *r2 = NULL;
        char *command = strtok_r(c, " ", &r2);
        if (strcmp(command, "turn") == 0)  // ignore "turn"
            command = strtok_r(NULL, " ", &r2);

        data.commands[data.commandCount].x1 = atoi(strtok_r(NULL, ",", &r2));
        data.commands[data.commandCount].y1 = atoi(strtok_r(NULL, " ", &r2));
        strtok_r(NULL, " ", &r2);  // ignore "through"
        data.commands[data.commandCount].x2 = atoi(strtok_r(NULL, ",", &r2));
        data.commands[data.commandCount].y2 = atoi(strtok_r(NULL, " ", &r2));

        switch (command[1]) {
        case 'n':  // on
            data.commands[data.commandCount].type = ON;
            break;
        case 'f':  // off
            data.commands[data.commandCount].type = OFF;
            break;
        case 'o':  // toggle
            data.commands[data.commandCount].type = TOGGLE;
        }

        ++data.commandCount;
    }

    pthread_t thread1;
    pthread_t thread2;

    pthread_create(&thread1, NULL, p1t, (void *)&data);
    pthread_create(&thread2, NULL, p2t, (void *)&data);

    unsigned int *p1;
    unsigned int *p2;

    pthread_join(thread1, (void **)&p1);
    pthread_join(thread2, (void **)&p2);

    printf("p1: %u\n", *p1);
    printf("p2: %u\n", *p2);

    printf("done in %f s\n", (double)(clock() - st) / CLOCKS_PER_SEC);

    free(p1);
    free(p2);

    free(input);
    fclose(fp);
}