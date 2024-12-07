#include <stdint.h>
#include <string.h>
#include <stdio.h>

uint64_t p1=0, p2=0;

uint64_t concat(uint64_t a, uint64_t b) {
  char buf[32];
  sprintf(buf, "%llu%llu", a, b);

  uint64_t output;
  sscanf(buf, "%llu", &output);

  return output;
}

int solve(uint64_t needed, unsigned count, uint64_t nums[static count], int concatUsed) {
  if (count < 2) {
    if (nums[0] != needed)
      return 0;

    p2 += needed;
    if (!concatUsed)
      p1 += needed;

    return 1;
  }

  uint64_t a = nums[0];
  uint64_t b = nums[1];

  int solved = 0;

  nums[1] = a + b;
  if ((solved = solve(needed, count-1, nums+1, concatUsed)))
    goto DONE;

  nums[1] = a * b;
  if ((solved = solve(needed, count-1, nums+1, concatUsed)))
    goto DONE;

  nums[1] = concat(a, b);
  solved = solve(needed, count-1, nums+1, 1);

DONE:
  nums[1] = b;
  return solved;
}

int main() {
  char line[64];
  while (fgets(line, 64, stdin) != NULL) {
    uint64_t needed;
    uint64_t nums[16];
    unsigned count = 0;

    char *start = line;
    sscanf(start, "%llu: ", &needed);
    while ((start = strchr(start+1, ' ')) != NULL)
      sscanf(start, " %llu ", nums + count++);

    solve(needed, count, nums, 0);
  }

  printf("%llu %llu\n", p1, p2);
}
