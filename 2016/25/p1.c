#include <string.h>
#include <stdio.h>

enum register_index { A=0, B=1, C=2, D=3 };

struct value {
    enum {
        INT,
        REGISTER
    } type;
    union {
        int value;
        enum register_index index;
    };
};

enum instruction {
    CPY,
    INC,
    DEC,
    JNZ,
    OUT
};

struct statement {
    enum instruction instruction;
    struct value x;
    struct value y;
};

struct statement PROGRAM[] = {

};

#define PROGRAM_LENGTH (sizeof PROGRAM / sizeof *PROGRAM)

void cpy(int *registers, struct value x, struct value y) {
    if (y.type == REGISTER)
        registers[y.index] = x.type == INT ? x.value : registers[x.index];
}

void inc(int *registers, struct value x) {
    if (x.type == REGISTER)
        ++registers[x.index];
}

void dec(int *registers, struct value x) {
    if (x.type == REGISTER)
        --registers[x.index];
}

void jnz(int *registers, struct value x, struct value y, int *pc) {
    if (x.type == INT ? x.value : registers[x.index])
        *pc += (y.type == INT ? y.value : registers[y.index]) - 1;
}

void out(int *registers, struct value x) {
    printf("%d", x.type == INT ? x.value : registers[x.index]);
    fflush(stdout);
}

void run(struct statement *program, int *registers) {
    for (int pc=0; pc >= 0 && pc < PROGRAM_LENGTH; ++pc) {
        struct statement statement = program[pc];
        switch (statement.instruction) {
            case INC: inc(registers, statement.x); break;
            case DEC: dec(registers, statement.x); break;
            case OUT: out(registers, statement.x); break;
            case JNZ: jnz(registers, statement.x, statement.y, &pc); break;
            case CPY: cpy(registers, statement.x, statement.y);
        }
    }
}

int main() {
    struct statement program_copy[PROGRAM_LENGTH];
    
    int *registers = (int [4]){7};
    memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    run(program_copy, registers);
    printf("%d ", registers[A]);
    // registers = (int [4]){12};
    // memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    // run(program_copy, registers);
    // printf("%d\n", registers[A]);
}
