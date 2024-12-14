/*
  https://docs.vlang.io/
  https://modules.vlang.io/
  https://github.com/vlang/v/discussions/17591

  run with
    v run a.v
  alternatively
    v -prod a.v && ./a
*/

import math
import os
import regex
import strconv

struct Grid {
  w int
  h int
}

struct Robot {
  pos struct {
    x int
    y int
  }
  v struct {
    x int
    y int
  }
}

fn parse_robot(s string) !Robot {
  mut digit_pattern := regex.regex_opt(r'-?\d+')!
  numbers := digit_pattern
    .find_all_str(s)
    .map(strconv.atoi(it)!)

  if numbers.len != 4 {
    return error("could not parse '${s}' into a robot")
  }

  return Robot{
    pos: struct { x: numbers[0], y: numbers[1] }
    v:   struct { x: numbers[2], y: numbers[3] }
  }
}

fn categorize(g Grid, r Robot) ?int {
  if r.pos.x == g.w / 2 || r.pos.y == g.h / 2 {
    return none
  }

  x := if r.pos.x < g.w / 2 { 0 } else { 1 << 0 }
  return x + (if r.pos.y < g.h / 2 { 0 } else { 1 << 1 })
}

fn simulate(g Grid, r Robot, n int) Robot {
  return Robot{
    ...r
    pos: struct {
      x: math.modulo_euclid(r.pos.x + r.v.x * n, g.w)
      y: math.modulo_euclid(r.pos.y + r.v.y * n, g.h)
    }
  }
}

fn solve_p1(g Grid, robots []Robot) int {
  categories := robots
    .map(simulate(g, it, 100))
    .map(categorize(g, it))
    .filter(it != none)

  mut counts := map[int]int{}
  for category in categories {
    counts[category]++
  }

  mut prod := 1
  for category in counts.values() {
    prod *= category
  }

  return prod
}

fn solve(a int, b int) (int, int, int) {
  if b == 0 {
    return a, 1, 0
  }

  gcd, s, t := solve(b, math.modulo_euclid(a, b))
  return gcd, t, s - a / b * t
}

fn find_lines(g Grid, robots []Robot, y_axis bool, start int) int {
  for time := start; true; time++ {
    mut counts := map[int]int{}
    for robot in robots.map(simulate(g, it, time)) {
      if y_axis {
        counts[robot.pos.y]++
      } else {
        counts[robot.pos.x]++
      }
    }

    line_count := counts.values().filter(it > 20).len
    if line_count >= 2 {
      return time
    }
  }

  panic('unreachable')
}

fn find_cycle(g Grid, robots []Robot, y_axis bool) (int, int) {
  start := find_lines(g, robots, y_axis, 0)
  end   := find_lines(g, robots, y_axis, start + 1)

  return start, end - start
}

fn solve_p2(g Grid, robots []Robot) int {
  h_start, h_len := find_cycle(g, robots, false)
  v_start, v_len := find_cycle(g, robots, true)

  gcd, s, _ := solve(h_len, v_len)
  k := (v_start - h_start) / gcd

  lcm := h_len * v_len / gcd

  return math.modulo_euclid(h_start + k*s * h_len, lcm)
}

fn main() {
  mut robots := []Robot{}
  for line in os.read_lines('input')! {
    if robot := parse_robot(line) {
      robots << robot
    } else {
      println(err)
    }
  }

  g := Grid{ w: 101, h: 103 }

  println(solve_p1(g, robots))
  println(solve_p2(g, robots))
}
