#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

typedef uint16_t (*op)(uint16_t);

struct thread_args {
    uint16_t *lights;
    op operation;
    size_t x1, y1, x2, y2;
};

static void die(char *cause) {
    perror(cause);
    exit(1);
}

static inline uint16_t on1(uint16_t n)     {return 1;            }
static inline uint16_t on2(uint16_t n)     {return n + 1;        }
static inline uint16_t off1(uint16_t n)    {return 0;            }
static inline uint16_t off2(uint16_t n)    {return n ? n - 1 : 0;}
static inline uint16_t toggle1(uint16_t n) {return !n;           }
static inline uint16_t toggle2(uint16_t n) {return n + 2;        }

static void *update(void *args) {
    struct thread_args *data = (struct thread_args *)args;
    
    for (size_t x=data->x1; x <= data->x2; ++x) {
        for (size_t y=data->y1; y <= data->y2; ++y) {
            data->lights[x*1000 + y] = data->operation(data->lights[x*1000 + y]);
        }
    }

    return NULL;
}

static void solve(char *input) {
    pthread_t thread1;
    pthread_t thread2;

    uint16_t lights1[1000 * 1000] = {0};
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

        struct thread_args args1 = {
            .lights = lights1,
            .x1 = x1, .y1 = y1, .x2 = x2, .y2 = y2
        };

        struct thread_args args2 = args1;
        args2.lights = lights2;

        switch (command[1]) {
        case 'n':  // on
            args1.operation = on1;
            args2.operation = on2;
            break;
        case 'f':  // off
            args1.operation = off1;
            args2.operation = off2;
            break;
        case 'o':  // toggle
            args1.operation = toggle1;
            args2.operation = toggle2;
        }

        pthread_create(&thread1, NULL, update, &args1);
        pthread_create(&thread2, NULL, update, &args2);

        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
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