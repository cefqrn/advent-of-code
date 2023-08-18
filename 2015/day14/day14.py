from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

from dataclasses import dataclass

@dataclass
class Deer:
    name: str
    speed: int
    fly_time: int
    rest_time: int

    is_flying: bool = True
    remaining_time: int = 0

    dist: int = 0
    points: int = 0

    def update(self):
        if self.is_flying:
            self.dist += self.speed

        self.remaining_time -= 1
        if self.remaining_time == 0:
            self.remaining_time = self.rest_time if self.is_flying else self.fly_time
            self.is_flying = not self.is_flying
    
    def __gt__(self, other: Deer):
        return self.dist > other.dist

deers: list[Deer] = []
for l in s.split('\n'):
    name, _, _, speed, _, _, fly_time, *_, rest_time, _ = l.split()
    deers.append(Deer(name, int(speed), int(fly_time), int(rest_time), True, int(fly_time)))

for i in range(2503):
    for deer in deers:
        deer.update()

    best: list[Deer] = []
    best_dist = 0
    for deer in deers:
        if deer.dist > best_dist:
            best_dist = deer.dist
            best = [deer]
        elif deer.dist == best_dist:
            best.append(deer)
    
    for deer in best:
        deer.points += 1

print(f'p1: {max(deers).dist}')
print(f'p2: {max(deers, key=lambda x: x.points).points}')