/*
  https://dlang.org/library/std/functional/memoize.html
  https://dlang.org/articles/ctod.html

  run with
    dmd a.d && ./a <input
*/

import std.algorithm;
import std.conv;
import std.functional;
import std.stdio;

ulong[] blink(ulong n) {
  if (n == 0)
    return [1];

  auto ns = to!string(n);
  auto l = ns.length;
  if (!(l & 1))
    return [
      to!ulong(ns[0..l/2]),
      to!ulong(ns[l/2..l])
    ];

  return [2024*n];
}

ulong solve(ulong n, uint iterations) {
  if (iterations == 0)
    return 1;

  return blink(n)
    .map!(n => memoize!solve(n, iterations-1))
    .sum();
}

int main() {
  auto f = File("input", "r");

  uint[] input;
  while (f.readf("%u ", input[input.length++])) {}
  input.length--;

  writefln("%u", input.map!(n => solve(n, 25)).sum());
  writefln("%u", input.map!(n => solve(n, 75)).sum());

  return 0;
}
