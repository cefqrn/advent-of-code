#include <stdlib.h>
#include <stdio.h>

#define SCANNER_COUNT 26

#define max(a, b) a > b ? a : b
#define min(a, b) a < b ? a : b

struct vec2 {
    int32_t x;
    int32_t y;
};

struct vec2_list {
    struct vec2 elements[SCANNER_COUNT];
    size_t count;
};

struct scanner {
    struct vec2 pos;
    int32_t beacon_dist;
};

int vec2_lt(struct vec2 *a, struct vec2 *b) {
    return a->x < b->x ?: a->x == b->x ? a->y < b->y : 0;
}

int vec2_eq(struct vec2 *a, struct vec2 *b) {
    return a->x == b->x && a->y == b->y;
}

int vec2_cmp(const void *a, const void *b) {
    struct vec2 *av = (struct vec2 *)a;
    struct vec2 *bv = (struct vec2 *)b;

    if (vec2_lt(av, bv)) return -1;
    if (vec2_eq(av, bv)) return  0;

    return 1;
}

void vec2_print(struct vec2 *p) {
    printf("(%d, %d)\n", p->x, p->y);
}

struct vec2_list combine_ranges(struct vec2_list ranges) {
    struct vec2_list newRanges = {0};

    struct vec2 prev = ranges.elements[0];
    for (size_t i=0; i < ranges.count; ++i) {
        struct vec2 curr = ranges.elements[i];
        if (prev.y < curr.x - 1) {
            newRanges.elements[newRanges.count++] = prev;
            prev = curr;
            continue;
        }

        prev = (struct vec2){prev.x, max(prev.y, curr.y)};
    }

    if (newRanges.count == 0 || !vec2_eq(&newRanges.elements[newRanges.count], &prev)) {
        newRanges.elements[newRanges.count++] = prev;
    }

    return newRanges;
}

int32_t get_next_int() {
    static char c = 0;
    char signChar;

    while (c < 48 || 57 < c) {
        signChar = c;
        c = getchar();
    }

    int32_t output = 0;
    do {
        output = output * 10 + c - 48;
        c = getchar();
    } while (48 <= c && c <= 57);

    return signChar == '-' ? -output: output;
}

int main() {
    struct scanner scanners[SCANNER_COUNT];
    struct vec2_list beacons = {0};

    for (size_t i=0; i < SCANNER_COUNT; ++i) {
        int32_t x, y, bx, by, dist;

        x = get_next_int();
        y = get_next_int();
        bx = get_next_int();
        by = get_next_int();

        dist = abs(x - bx) + abs(y - by);

        struct vec2 beacon = {bx, by};

        int beacon_exists = 0;
        for (size_t j=0; j < beacons.count; ++j) {
            if (vec2_eq(&beacons.elements[j], &beacon)) {
                beacon_exists = 1;
                break;
            }
        }
        
        if (!beacon_exists)
            beacons.elements[beacons.count++] = beacon;


        scanners[i].pos.x = x;
        scanners[i].pos.y = y;
        scanners[i].beacon_dist = dist;
    }

    struct vec2_list ranges = {0};
    int32_t h = 2000000;
    for (size_t i=0; i < SCANNER_COUNT; ++i) {
        struct scanner s = scanners[i];

        int32_t dh = abs(s.pos.y - h);
        if (dh > s.beacon_dist)
            continue;

        struct vec2 r = {
            .x = s.pos.x - (s.beacon_dist - dh),
            .y = s.pos.x + (s.beacon_dist - dh)
        };

        ranges.elements[ranges.count++] = r;
    }

    qsort(ranges.elements, ranges.count, sizeof(*ranges.elements), vec2_cmp);
    struct vec2_list combinedRanges = combine_ranges(ranges);

    uint32_t s = 0;
    for (size_t i=0; i < combinedRanges.count; ++i) {
        struct vec2 r = combinedRanges.elements[i];
        s += r.y - r.x + 1;

        for (size_t i=0; i < SCANNER_COUNT; ++i) {
            struct vec2 beacon = beacons.elements[i];
            s -= beacon.y == h && r.x < beacon.x && beacon.x <= r.y;
        }
    }

    printf("%d\n", s);
}