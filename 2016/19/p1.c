#include <stdlib.h>
#include <stdio.h>

#define ELF_COUNT 3014603

typedef struct node {
  unsigned value;
  struct node *next;
} node;

void init(unsigned elfCount, node elves[static elfCount]) {
  for (unsigned i=0; i < elfCount; ++i) {
    elves[i] = (node){
      .value = i + 1,
      .next = elves + i + 1
    };
  }
  elves[elfCount - 1].next = elves;
}

unsigned p1(node elves[static 1]) {
  while (elves->next != elves)
    elves = elves->next = elves->next->next;

  return elves->value;
}

unsigned p2(unsigned elfCount, node elves[static elfCount]) {
  for (unsigned i=0; i < elfCount / 2 - 1; ++i)
    elves = elves->next;

  unsigned isEven = !(elfCount & 1);
  while (elves->next != elves) {
    elves->next = elves->next->next;
    isEven = !isEven;
    if (isEven)
      elves = elves->next;
  }

  return elves->value;
}

int main() {
  struct node *elves = malloc(ELF_COUNT * sizeof *elves);
  if (elves == NULL) {
    fprintf(stderr, "could not allocate memory for elves");
    return 1;
  }

  init(ELF_COUNT, elves);
  unsigned a = p1(elves);

  init(ELF_COUNT, elves);
  unsigned b = p2(ELF_COUNT, elves);

  printf("%u %u\n", a, b);

  free(elves);
  return 0;
}
