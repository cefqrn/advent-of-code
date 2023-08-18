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

struct statement;
typedef void (*instruction_t)(struct statement *program, int *registers, int *pc, struct value x, struct value y);
struct statement {
    instruction_t instruction;
    struct value x;
    struct value y;
};

void cpy(struct statement *program, int *registers, int *pc, struct value x, struct value y);
void inc(struct statement *program, int *registers, int *pc, struct value x, struct value y);
void dec(struct statement *program, int *registers, int *pc, struct value x, struct value y);
void jnz(struct statement *program, int *registers, int *pc, struct value x, struct value y);
void tgl(struct statement *program, int *registers, int *pc, struct value x, struct value y);

struct statement PROGRAM[] = {
    {.instruction = cpy, .x = {REGISTER,   A}, .y = {REGISTER,  B}},
    {.instruction = dec, .x = {REGISTER,   B}},
    {.instruction = cpy, .x = {REGISTER,   A}, .y = {REGISTER,  D}},
    {.instruction = cpy, .x = {INT,        0}, .y = {REGISTER,  A}},
    {.instruction = cpy, .x = {REGISTER,   B}, .y = {REGISTER,  C}},
    {.instruction = inc, .x = {REGISTER,   A}},
    {.instruction = dec, .x = {REGISTER,   C}},
    {.instruction = jnz, .x = {REGISTER,   C}, .y = {INT,      -2}},
    {.instruction = dec, .x = {REGISTER,   D}},
    {.instruction = jnz, .x = {REGISTER,   D}, .y = {INT,      -5}},
    {.instruction = dec, .x = {REGISTER,   B}},
    {.instruction = cpy, .x = {REGISTER,   B}, .y = {REGISTER,  C}},
    {.instruction = cpy, .x = {REGISTER,   C}, .y = {REGISTER,  D}},
    {.instruction = dec, .x = {REGISTER,   D}},
    {.instruction = inc, .x = {REGISTER,   C}},
    {.instruction = jnz, .x = {REGISTER,   D}, .y = {INT,      -2}},
    {.instruction = tgl, .x = {REGISTER,   C}},
    {.instruction = cpy, .x = {INT,      -16}, .y = {REGISTER,  C}},
    {.instruction = jnz, .x = {INT,        1}, .y = {REGISTER,  C}},
    {.instruction = cpy, .x = {INT,       71}, .y = {REGISTER,  C}},
    {.instruction = jnz, .x = {INT,       75}, .y = {REGISTER,  D}},
    {.instruction = inc, .x = {REGISTER,   A}},
    {.instruction = inc, .x = {REGISTER,   D}},
    {.instruction = jnz, .x = {REGISTER,   D}, .y = {INT,      -2}},
    {.instruction = inc, .x = {REGISTER,   C}},
    {.instruction = jnz, .x = {REGISTER,   C}, .y = {INT,      -5}},
};

#define PROGRAM_LENGTH (sizeof PROGRAM / sizeof *PROGRAM)

void cpy(struct statement *program, int *registers, int *pc, struct value x, struct value y) {
    if (y.type == REGISTER)
        registers[y.index] = x.type == INT ? x.value : registers[x.index];
}

void inc(struct statement *program, int *registers, int *pc, struct value x, struct value y) {
    if (x.type == REGISTER)
        ++registers[x.index];
}

void dec(struct statement *program, int *registers, int *pc, struct value x, struct value y) {
    if (x.type == REGISTER)
        --registers[x.index];
}

void jnz(struct statement *program, int *registers, int *pc, struct value x, struct value y) {
    if (x.type == INT ? x.value : registers[x.index])
        *pc += (y.type == INT ? y.value : registers[y.index]) - 1;
}

void tgl(struct statement *program, int *registers, int *pc, struct value x, struct value y) {
    int tp = *pc + (x.type == INT ? x.value : registers[x.index]);

    if (tp < 0 || tp >= PROGRAM_LENGTH)
        return;

    instruction_t instruction = program[tp].instruction;
    if (instruction == inc) {
        program[tp].instruction = dec;
    } else if (instruction == dec || instruction == tgl) {
        program[tp].instruction = inc;
    } else if (instruction == jnz) {
        program[tp].instruction = cpy;
    } else {
        program[tp].instruction = jnz;
    }
}

int main() {
    struct statement program_copy[PROGRAM_LENGTH];
    
    memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    int *registers = (int []){7, 0, 0, 0};
    for (int pc=0; pc < PROGRAM_LENGTH; ++pc) {
        struct statement statement = program_copy[pc];
        statement.instruction(program_copy, registers, &pc, statement.x, statement.y);
    }
    printf("%d ", registers[A]);

    registers = (int []){12, 0, 0, 0};
    memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    for (int pc=0; pc < PROGRAM_LENGTH; ++pc) {
        struct statement statement = program_copy[pc];
        statement.instruction(program_copy, registers, &pc, statement.x, statement.y);
    }
    printf("%d\n", registers[A]);
}
