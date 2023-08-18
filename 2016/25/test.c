#include <stdio.h>

#define SOLUTION 196

int main() {
    while (1) {
        int a = SOLUTION + 362 * 7;
        do {
            printf("%d", a & 1);
        } while ((a >>= 1));
    }
}
