// https://en.wikipedia.org/wiki/C_string_handling
// https://en.cppreference.com/w/c/
// https://gcc.gnu.org/onlinedocs/cpp/Macros.html
//
// run with
//   gcc -Wall -Werror -pedantic c.c && ./a.out

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HANDLE_COLUMN(operation, initial) { \
  accumulator1 = initial; \
  for (unsigned j=0; j < lineCount-1; ++j) \
    accumulator1 = accumulator1 operation atoi(input + lineLength*j + columnStart); \
 \
  accumulator2 = initial; \
  for (unsigned j=columnStart; j < columnEnd; ++j) { \
    unsigned long long n = 0; \
    for (unsigned k=0; k < lineCount-1; ++k) { \
      char c = input[lineLength*k + j]; \
      if (c != ' ') \
        n = n*10 + (c - '0'); \
    } \
 \
    accumulator2 = accumulator2 operation n; \
  } \
}

int main(void) {
  char *input;
  long fileSize;
  {  // read file into memory
    FILE *f = fopen("input", "r");

    fseek(f, 0, SEEK_END);
    fileSize = ftell(f);
    fseek(f, 0, SEEK_SET);

    input = malloc((fileSize + 1) * sizeof (char));
    input[fileSize] = 0;

    size_t read = fread(input, sizeof (char), fileSize, f);
    assert(read == fileSize);

    fclose(f);
  }


  unsigned lineLength;
  unsigned lineCount;
  {
    char *firstNewlineIndex = strchr(input, '\n');
    lineLength = firstNewlineIndex - input + 1;

    // fileSize + 1 in case the input doesn't have a trailing newline
    lineCount = (fileSize + 1) / lineLength;
  }


  // delimiter -> operator / end of line/file
  size_t delimiterIndices[1000];
  size_t delimiterCount = 0;
  for (unsigned i=0; i < lineLength; ++i) {
    switch (input[lineLength*(lineCount-1) + i]) {
    case '+':
    case '*':
    case '\0':
    case '\n':
      delimiterIndices[delimiterCount++] = i;
    case ' ':
      break;
    default:
      assert("invalid operator" && 0);
    }
  }
  // act as if there's another space before an operator
  delimiterIndices[delimiterCount-1]++;


  unsigned long long p1 = 0;
  unsigned long long p2 = 0;
  for (unsigned i=0; i < delimiterCount-1; ++i) {
    size_t columnStart = delimiterIndices[i  ];
    size_t columnEnd   = delimiterIndices[i+1]-1;

    char operator = input[lineLength*(lineCount-1) + columnStart];

    unsigned long long accumulator1;
    unsigned long long accumulator2;
    switch (operator) {
    case '+': HANDLE_COLUMN(+, 0); break;
    case '*': HANDLE_COLUMN(*, 1); break;
    default: assert("invalid operator" && 0);
    }

    p1 += accumulator1;
    p2 += accumulator2;
  }

  printf("%llu %llu\n", p1, p2);

  free(input);
}
