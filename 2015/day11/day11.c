#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define PASSWORD_LENGTH 8

const short INVALID[3] = {8, 11, 14};

static void die(const char *cause) {
    puts(cause);
    exit(EXIT_FAILURE);
}

static void print_pass(const short pass[PASSWORD_LENGTH]) {
    for (size_t i=0; i < PASSWORD_LENGTH; ++i) {
        printf("%c", pass[i] + 97);
    }
    printf("\n");
}

static int has_straight(const short pass[PASSWORD_LENGTH]) {
    for (size_t i=0; i < PASSWORD_LENGTH - 3; ++i) {
        if (pass[i] == pass[i + 1] - 1 && pass[i] == pass[i + 2] - 2)
            return 1;
    }

    return 0;
}

static int has_pairs(const short pass[PASSWORD_LENGTH]) {
    short count = 0;
    for (size_t i=0; i < PASSWORD_LENGTH - 1; ++i) {
        if (pass[i] == pass[i + 1]) {
            ++count;
            ++i;
        }
    }

    return count >= 2;
}

static int has_no_invalid_chars(const short pass[PASSWORD_LENGTH]) {
    for (size_t i=0; i < PASSWORD_LENGTH; ++i) {
        for (size_t j=0; j < 3; ++j) {
            if (pass[i] == INVALID[j])
                return 0;
        }
    }

    return 1;
}

static int is_valid(const short pass[PASSWORD_LENGTH]) {
    return has_no_invalid_chars(pass) && has_straight(pass) && has_pairs(pass);
}

static short *increment_pass(short pass[PASSWORD_LENGTH]) {
    for (size_t i=PASSWORD_LENGTH-1; i >= 0; --i) {
        if (pass[i] < 25) {
            ++pass[i];
            return pass;
        }

        pass[i] = 0;
    }

    return pass;
}

int main(int argc, char *argv[]) {
    if (argc != 2)
        die("no initial password given");

    if (strlen(argv[1]) != PASSWORD_LENGTH)
        die("invalid initial password");

    short pass[PASSWORD_LENGTH];
    for (size_t i=0; i < PASSWORD_LENGTH; ++i) {
        pass[i] = argv[1][i] - 97;
    }

    while (!is_valid(pass)) increment_pass(pass);
    printf("p1: ");
    print_pass(pass);

    increment_pass(pass);
    while (!is_valid(pass)) increment_pass(pass);

    printf("p2: ");
    print_pass(pass);
}