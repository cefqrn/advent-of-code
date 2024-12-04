"""
initially solved 2023-12
data now reads from an input file
added comments
"""

data = """
[...]
"""
from pathlib import Path
data = (Path(__file__).parent / "input").read_text()

lines = data.strip().splitlines()
from re import findall

stones = []
for line in lines:
  stones.append(tuple(map(int, findall(r"-?\d+", line))))

from fractions import Fraction

a, b = stones[:2]
ax, ay, az, avx, avy, avz = a
bx, by, bz, bvx, bvy, bvz = b

"""
initial velocity found using desmos
https://www.desmos.com/calculator/kehld018vx (example input)
s is the speed of the rock being thrown

if the rock collides with a hailstone,
then that hailstone's trajectory relative to the rock
needs to cross the origin
since all of the hailstones collide with the rock,
all of the trajectories need to intersect in the same spot

in other words, if we look at things from the rock's point of view
and act as if it isn't moving
then all of the hailstones need to aim at and hit the rock's position

the intersections in the graph are the rock's position

since desmos didn't have a 3d calculator at the time,
it was used to show the trajectories on the xy and yz planes
"""
avx -= 154
bvx -= 154
avy -= 75
bvy -= 75
avz -= 290
bvz -= 290

x = bx - ax
y = by - ay

d = avx * -bvy + bvx * avy
t = Fraction(-bvy*x + bvx*y, d)

print(sum((
  ax + avx*t,
  ay + avy*t,
  az + avz*t
)))