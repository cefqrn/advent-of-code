#include <stdio.h>

#define LABEL_AT(line, index) (((line[index] - 65) << 10) | ((line[index + 1] - 65) << 5) | (line[index + 2] - 65) | ((line[index + 2] == 'Z') << 15))
#define END_LABEL 0x8000

typedef unsigned short label;

typedef union {
    struct {
        label left;
        label right;
    };
    label next[2];
} node;

int main() {
    FILE *file = fopen("08/input", "r");

    // load instructions
    unsigned char instructions[1024] = {0};
    unsigned instructionCount = 0;
    {
        char c;
        while ((c = fgetc(file)) != '\n')
            instructions[instructionCount++] = c == 'R';

        // ignore second newline
        (void)fgetc(file);
    }

    // parse nodes
    node nodes[65536] = {0};
    label currentNodes[32] = {0};
    unsigned currentNodeCount = 0;
    {
        char line[32];
        while (fgets(line, 32, file) != NULL) {
            label currentLabel = LABEL_AT(line, 0);

            nodes[currentLabel] = (node){
                .left  = LABEL_AT(line, 7),
                .right = LABEL_AT(line, 12)
            };

            if (line[2] == 'A')
                currentNodes[currentNodeCount++] = currentLabel;
        }
    }

    unsigned long long stepCount = 0;
    while (1) {
        for (unsigned instructionIndex=0; instructionIndex < instructionCount; ++instructionIndex) {
            unsigned char instruction = instructions[instructionIndex];

            unsigned short allEndNodes = END_LABEL;
            for (unsigned i=0; i < currentNodeCount; ++i) {
                label currentLabel = currentNodes[i];
                allEndNodes &= currentLabel;

                currentNodes[i] = nodes[currentLabel].next[instruction];
            }

            if (allEndNodes)
                goto END;

            stepCount++;
        }
    }

    END:
    printf("%llu\n", stepCount);

    fclose(file);
}
