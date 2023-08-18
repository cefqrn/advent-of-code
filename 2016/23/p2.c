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
    TGL
};

struct statement {
    enum instruction instruction;
    struct value x;
    struct value y;
};

struct statement PROGRAM[] = {
    {CPY, .x = {REGISTER,   A}, .y = {REGISTER,  B}},
    {DEC, .x = {REGISTER,   B}},
    {CPY, .x = {REGISTER,   A}, .y = {REGISTER,  D}},
    {CPY, .x = {INT,        0}, .y = {REGISTER,  A}},
    {CPY, .x = {REGISTER,   B}, .y = {REGISTER,  C}},
    {INC, .x = {REGISTER,   A}},
    {DEC, .x = {REGISTER,   C}},
    {JNZ, .x = {REGISTER,   C}, .y = {INT,      -2}},
    {DEC, .x = {REGISTER,   D}},
    {JNZ, .x = {REGISTER,   D}, .y = {INT,      -5}},
    {DEC, .x = {REGISTER,   B}},
    {CPY, .x = {REGISTER,   B}, .y = {REGISTER,  C}},
    {CPY, .x = {REGISTER,   C}, .y = {REGISTER,  D}},
    {DEC, .x = {REGISTER,   D}},
    {INC, .x = {REGISTER,   C}},
    {JNZ, .x = {REGISTER,   D}, .y = {INT,      -2}},
    {TGL, .x = {REGISTER,   C}},
    {CPY, .x = {INT,      -16}, .y = {REGISTER,  C}},
    {JNZ, .x = {INT,        1}, .y = {REGISTER,  C}},
    {CPY, .x = {INT,       71}, .y = {REGISTER,  C}},
    {JNZ, .x = {INT,       75}, .y = {REGISTER,  D}},
    {INC, .x = {REGISTER,   A}},
    {INC, .x = {REGISTER,   D}},
    {JNZ, .x = {REGISTER,   D}, .y = {INT,      -2}},
    {INC, .x = {REGISTER,   C}},
    {JNZ, .x = {REGISTER,   C}, .y = {INT,      -5}},
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

void tgl(int *registers, struct value x, int *pc, struct statement *program) {
    int tp = *pc + (x.type == INT ? x.value : registers[x.index]);

    if (tp < 0 || tp >= PROGRAM_LENGTH)
        return;

    switch (program[tp].instruction) {
        case INC: program[tp].instruction = DEC; break;
        case DEC:
        case TGL: program[tp].instruction = INC; break;
        case JNZ: program[tp].instruction = CPY; break;
        case CPY: program[tp].instruction = JNZ;
    }
}

void run(struct statement *program, int *registers) {
    for (int pc=0; pc >= 0 && pc < PROGRAM_LENGTH; ++pc) {
        struct statement statement = program[pc];
        switch (statement.instruction) {
            case INC: inc(registers, statement.x); break;
            case DEC: dec(registers, statement.x); break;
            case TGL: tgl(registers, statement.x, &pc, program); break;
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

    registers = (int [4]){12};
    memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    run(program_copy, registers);
    printf("%d\n", registers[A]);
}
