#include <sys/mman.h>
#include <sys/stat.h>
#include <stdint.h>
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
    static char c = 0;
    char signChar;

    while ('9' < c || c < '0') {
        signChar = c;
        c = getchar_unlocked();
    }

    int output = 0;
    do {
        output = output * 10 + c - 48;
        c = getchar_unlocked();
    } while ('0' <= c && c <= '9');

    return signChar == '-' ? -output: output;
}

int main() {
    struct timespec startParsing, start, end;
    timespec_get(&startParsing, TIME_UTC);

    struct stat sb;
    fstat(STDIN_FILENO, &sb);

    char *input = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, STDIN_FILENO, 0);
    size_t inputIndex = 0;

    struct scanner scanners[SCANNER_COUNT];
    int aRanges[SCANNER_COUNT][2];
    int bRanges[SCANNER_COUNT][2];

    for (int i=0; i < SCANNER_COUNT; ++i) {
        int x=0, y=0, bx=0, by=0;

        inputIndex += 12;
        int sign = input[inputIndex++] == '-' ? -1 : 1;
        inputIndex -= sign > 0;
        for (char c=input[inputIndex++]; c >= '0'; c=input[inputIndex++])
            x = x * 10 + c - 48;
        x *= sign;
        
        inputIndex += 3;
        sign = input[inputIndex++] == '-' ? -1 : 1;
        inputIndex -= sign > 0;
        for (char c=input[inputIndex++]; c <= '9'; c=input[inputIndex++])
            y = y * 10 + c - 48;
        y *= sign;

        inputIndex += 24;
        sign = input[inputIndex++] == '-' ? -1 : 1;
        inputIndex -= sign > 0;
        for (char c=input[inputIndex++]; c >= '0'; c=input[inputIndex++])
            bx = bx * 10 + c - 48;
        bx *= sign;

        inputIndex += 3;
        sign = input[inputIndex++] == '-' ? -1 : 1;
        inputIndex -= sign > 0;
        for (char c=input[inputIndex++]; c >= '0'; c=input[inputIndex++])
            by = by * 10 + c - 48;
        by *= sign;

        // printf("%d, %d  %d, %d\n", x, y, bx, by);

        // x = get_next_int();
        // y = get_next_int();
        // bx = get_next_int();
        // by = get_next_int();

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

    timespec_get(&start, TIME_UTC);

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

    timespec_get(&end, TIME_UTC);
    long unsigned timeWithParsing = end.tv_nsec - startParsing.tv_nsec;
    long unsigned timeWithoutParsing = end.tv_nsec - start.tv_nsec;

    printf("(%d, %d) %lu\n", x, y, (long unsigned)x * 4000000 + y);
    printf("time: %ld µs with parsing\n", timeWithParsing/1000);
    printf("time: %ld µs without parsing\n", timeWithoutParsing/1000);
}