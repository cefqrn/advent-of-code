#include <mach/mach_time.h>
#include <mach/mach.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>

#define SCANNER_COUNT 26

struct scanner {
    int dist;
    int x;
    int y;
};

int get_next_int() {
    static char *input = NULL;
    static size_t inputIndex = 0;

    if (input == NULL) {
        struct stat sb;
        fstat(STDIN_FILENO, &sb);

        input = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, STDIN_FILENO, 0);
    }

    static char c = 0;
    char signChar;

    while ('9' < c || c < '0') {
        signChar = c;
        c = input[inputIndex++];
    }

    int output = 0;
    do {
        output = output * 10 + c - 48;
        c = input[inputIndex++];
    } while ('0' <= c && c <= '9');

    return signChar == '-' ? -output: output;
}

int main() {
    long unsigned startParsing = mach_absolute_time();

    size_t inputIndex = 0;

    struct scanner scanners[SCANNER_COUNT];
    int aRanges[SCANNER_COUNT][2];
    int bRanges[SCANNER_COUNT][2];

    for (int i=0; i < SCANNER_COUNT; ++i) {
        int x=0, y=0, bx=0, by=0;

        x = get_next_int();
        y = get_next_int();
        bx = get_next_int();
        by = get_next_int();

        unsigned dist = abs(x - bx) + abs(y - by);

        scanners[i] = (struct scanner){
            .dist = abs(x - bx) + abs(y - by),
            .x = x,
            .y = y
        };

        aRanges[i][0] = y-x-dist;
        aRanges[i][1] = y-x+dist;

        bRanges[i][0] = y+x-dist;
        bRanges[i][1] = y+x+dist;
    }

    long unsigned start = mach_absolute_time();

    int aCandidates[2 * SCANNER_COUNT] = {0};
    int bCandidates[2 * SCANNER_COUNT] = {0};
    int aCandidateCount = 0;
    int bCandidateCount = 0;
    for (int i=0; i < SCANNER_COUNT-1; ++i) {
        for (int j=i+1; j < SCANNER_COUNT; ++j) {
            if (aRanges[i][1] + 2 == aRanges[j][0])
                aCandidates[aCandidateCount++] = aRanges[i][1] + 1;
            if (aRanges[j][1] + 2 == aRanges[i][0])
                aCandidates[aCandidateCount++] = aRanges[j][1] + 1;

            if (bRanges[i][1] + 2 == bRanges[j][0])
                bCandidates[bCandidateCount++] = bRanges[i][1] + 1;
            if (bRanges[j][1] + 2 == bRanges[i][0])
                bCandidates[bCandidateCount++] = bRanges[j][1] + 1;
        }
    }

    int x, y;
    for (int i=0; i < aCandidateCount; ++i) {
        for (int j=0; j < bCandidateCount; ++j) {
            int p2x = bCandidates[j] - aCandidates[i];
            if (p2x & 1) continue;

            int px = p2x >> 1;
            int py = px + aCandidates[i];

            for (int k=0; k < SCANNER_COUNT; ++k) {
                if (abs(scanners[k].x - px) + abs(scanners[k].y - py) <= scanners[k].dist) {
                    goto EXIT;
                }
            }

            x = px;
            y = py;

            goto END;

            EXIT:;
        }
    }

    END:;

    long unsigned end = mach_absolute_time();

    mach_timebase_info_data_t timebase = {0};
    mach_timebase_info(&timebase);

    long unsigned timeWithParsing =    (end - startParsing) * (long unsigned)timebase.numer / (long unsigned)timebase.denom;
    long unsigned timeWithoutParsing = (end - start       ) * (long unsigned)timebase.numer / (long unsigned)timebase.denom;

    printf("(%d, %d) %lu\n", x, y, (long unsigned)x * 4000000 + y);
    printf("time: %ld ns with parsing\n", timeWithParsing);
    printf("time: %ld ns without parsing\n", timeWithoutParsing);
}
