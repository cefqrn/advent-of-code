#!/bin/bash

if [ $# -ne 1 ]; then
    echo $0 "<input>"
    exit
fi

folder=`mktemp -d`
code="$folder/code.c"

cat > $code <<END
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
END

while read -r line
do
    tokens=(`echo $line | tr '[:lower:]' '[:upper:]'`)
    echo -n "    { ${tokens[0]}, " >> $code
    for ((i=1; i < ${#tokens[@]}; ++i)); do
        x=${tokens[i]}
        if [[ "ABCD" =~ $x ]]; then
            echo -n "{ REGISTER, $x }, " >> $code
        else
            echo -n "{ INT, $x }, " >> $code
        fi
    done
    echo }, >> $code
done < $1

cat >> $code <<END
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
    fflush(stdout);

    registers = (int [4]){12};
    memcpy(program_copy, PROGRAM, sizeof PROGRAM);
    run(program_copy, registers);
    printf("%d\n", registers[A]);
}
END

gcc -O3 -std=c11 $code -o "$folder/prog" && (time "$folder/prog" & echo running in $code & wait)
rm -r $folder
