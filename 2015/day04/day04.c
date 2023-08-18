#include "md5.h"
#include <stdatomic.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <math.h>

#define THREAD_COUNT 4
#define BUFFER_SIZE 32
#define PREFIX 0x00FFFFFF

struct data {
    size_t limit;
    char *key;
    atomic_size_t num;
    atomic_size_t min;
};

size_t concat_number(char *buffer, char *key, unsigned int num) {
    size_t i = 0;
    while ((buffer[i] = key[i]))
        ++i;

    size_t j=0;
    char numBuffer[BUFFER_SIZE];
    while (num) {
        numBuffer[j++] = num % 10 + 48;
        num /= 10;
    }

    while (j) {
        buffer[i++] = numBuffer[--j];
    }

    // buffer[i] = 0;

    return i;
}

void *find_num(void *args) {
    struct data *d = args;
    
    for (size_t i=d->num++; d->num < d->limit && !d->min; i=d->num++) {
        char buffer[BUFFER_SIZE];
        size_t len = concat_number(buffer, d->key, i);
        // snprintf(buffer, BUFFER_SIZE, "%s%zu", d->key, i);

        if (!(((uint32_t *)md5(buffer, len))[0] & PREFIX)) {
            if (!d->min || i < d->min) {
                d->min = i;
            }

            return NULL;
        }
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        puts("usage: ./main <key> <limit>");
        return 1;
    }

    atomic_size_t num = 0, min = 0;
    struct data d = {
        .limit = atoi(argv[2]),
        .key = argv[1],
        .num = num,
        .min = min
    };

    size_t processorCount = sysconf(_SC_NPROCESSORS_ONLN);
    
    pthread_t *threads = malloc(processorCount * sizeof *threads);
    for (size_t i=0; i < processorCount; ++i) {
        pthread_create(&threads[i], NULL, find_num, (void *)&d);
    }

    for (size_t i=0; i < processorCount; ++i) {
        pthread_join(threads[i], NULL);
    }

    if (d.min) {
        printf("%zu\n", d.min);
    } else {
        puts("no answer found within the specified range");
    }
}
