#[
  https://learnxinyminutes.com/nim/
  https://nim-lang.org/docs/manual.html
  https://nimbyexample.com/

  run with
    nim r a.nim
  alternatively
    nim r -d:release a.nim
]#

import std/enumerate
import std/heapqueue
import std/sequtils
import std/sets
import std/tables

type
  Position     = tuple[x: int, y: int]
  Displacement = tuple[x: int, y: int]
  Direction = enum north, east, south, west
  Pose = tuple[pos: Position, dir: Direction]
  State = tuple[score: int, p: Pose, history: HashSet[Position]]

func left(dir: Direction): Direction =
  return (if dir == north: west else: dir.pred)

func right(dir: Direction): Direction =
  return (if dir == west: north else: dir.succ)

func displacement(dir: Direction): Displacement =
  case dir
  of north: return ( 0, -1)
  of east:  return ( 1,  0)
  of south: return ( 0,  1)
  of west:  return (-1,  0)

func `+`(pos: Position, d: Displacement): Position =
  return (pos.x + d.x, pos.y + d.y)

func `+`(pos: Position, d: Direction): Position =
  return pos + d.displacement

func `<`(a: State, b: State): bool =
  return a.score < b.score

func ahead(p: Pose): Pose =
  return (p.pos + p.dir, p.dir)

func left(p: Pose): Pose =
  return (p.pos, p.dir.left).ahead

func right(p: Pose): Pose =
  return (p.pos, p.dir.right).ahead

func next(s: State): seq[State] =
  return @[
    (s.score + 1, s.p.ahead, s.history + toHashSet([s.p.ahead.pos])),
    (s.score + 1001, s.p.right, s.history + toHashSet([s.p.right.pos])),
    (s.score + 1001, s.p.left,  s.history + toHashSet([s.p.left.pos ]))
  ]

var
  grid = initTable[Position, char]()
  ipos: Position
  epos: Position

for (y, line) in enumerate("input".lines):
  for (x, c) in enumerate(line):
    var pos = (x, y)

    grid[pos] = c
    if c == 'S':
      ipos = pos
    if c == 'E':
      epos = pos

var
  ip = (ipos, east)
  istate = (0, ip, toHashSet[Position]([ipos]))
  in_best = initHashSet[Position]()
  remaining = toHeapQueue[State]([istate])
  seen = toTable[Pose, int]({ip: 0})
  best = -1

proc shouldCheck(s: State): bool =
  if grid[s.p.pos] == '#':
    return false

  if s.p in seen and s.score > seen[s.p]:
    return false

  return true

while remaining.len > 0:
  let curr = remaining.pop

  if best != -1 and curr.score > best:
    continue

  if curr.p.pos == epos:
    in_best = in_best.union(curr.history)
    if best == -1:
      echo curr.score
      best = curr.score

    continue

  for s in curr.next.filter(shouldCheck):
    seen[s.p] = s.score
    remaining.push(s)

echo in_best.len
