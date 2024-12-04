#!/usr/bin/awk -f

function count(string, pattern) {
  c = 0
  while (i = match(string, pattern)) {
    string = substr(string, i+1)  # allow overlap
    c++
  }

  return c
}

{
  contents = $0
  w = length(contents)

  while (getline > 0)
    contents = contents " " $0
}

END {
  p1 = p2 = 0

  p1 += count(contents, "XMAS")
  p1 += count(contents, "SAMX")
  for (dl = -1; dl <= 1; dl++) {
    p1 += count(contents, "X.{" (w+dl) "}M.{" (w+dl) "}A.{" (w+dl) "}S")
    p1 += count(contents, "S.{" (w+dl) "}A.{" (w+dl) "}M.{" (w+dl) "}X")
  }

  p2 += count(contents, "M.M.{" (w-1) "}A.{" (w-1) "}S.S")
  p2 += count(contents, "S.M.{" (w-1) "}A.{" (w-1) "}S.M")
  p2 += count(contents, "S.S.{" (w-1) "}A.{" (w-1) "}M.M")
  p2 += count(contents, "M.S.{" (w-1) "}A.{" (w-1) "}M.S")

  print p1 " " p2
}
