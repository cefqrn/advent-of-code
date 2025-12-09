// https://docs.carbon-lang.dev/
// https://github.com/carbon-language/carbon-lang/tree/trunk
// and thanks to @savagepastaman on the python discord server
//
// run on http://carbon.compiler-explorer.com/

import Core library "io";
import Core library "range";

var k: i32 = 8;

fn Range(start: i32, end: i32) -> Core.IntRange(32) {
  // undefined symbol: _CInclusiveRange.Core
  return Core.IntRange(32).Make(start, end);
}

fn Abs(x: i32) -> i32 {
  if (x < 0) {
    return -x;
  } else {
    return  x;
  }
}

fn Min(a: i32, b: i32) -> i32 {
  if (a <= b) {
    return a;
  } else {
    return b;
  }
}

fn Max(a: i32, b: i32) -> i32 {
  if (a >= b) {
    return a;
  } else {
    return b;
  }
}

fn IsValidRectangle(coordinates: array((i32, i32), 8), i: i32, j: i32) -> bool {
  let x_bounds: (i32, i32) = (
    Min(coordinates[i].0, coordinates[j].0),
    Max(coordinates[i].0, coordinates[j].0)
  );

  let y_bounds: (i32, i32) = (
    Min(coordinates[i].1, coordinates[j].1),
    Max(coordinates[i].1, coordinates[j].1)
  );

  var a: i32 = i;
  var b: i32 = i+1;
  while (b != i) {
    let p: (i32, i32) = coordinates[a];
    let q: (i32, i32) = coordinates[b];

    let xs: (i32, i32) = (Min(p.0, q.0), Max(p.0, q.0));
    let ys: (i32, i32) = (Min(p.1, q.1), Max(p.1, q.1));

    if (xs.0 == xs.1 and x_bounds.0 < xs.0 and xs.1 < x_bounds.1) {
      if ((ys.0 <= y_bounds.0 and y_bounds.0 <  ys.1)
       or (ys.0 <  y_bounds.1 and y_bounds.1 <= ys.1)
       or (y_bounds.0 <  ys.0 and ys.0 <  y_bounds.1)
       or (y_bounds.0 <  ys.1 and ys.1 <  y_bounds.1)) {
        return false;
      }
    } else if (y_bounds.0 < ys.0 and ys.1 < y_bounds.1) {
      if ((xs.0 <= x_bounds.0 and x_bounds.0 <  xs.1)
       or (xs.0 <  x_bounds.1 and x_bounds.1 <= xs.1)
       or (x_bounds.0 <  xs.0 and xs.0 <  x_bounds.1)
       or (x_bounds.0 <  xs.1 and xs.1 <  x_bounds.1)) {
        return false;
      }
    }

    a = (a+1) % k;
    b = (b+1) % k;
  }

  return true;
}

fn PrintI64(n: i64) {
  var output: array(char, 20);
  var length: i32 = 0;

  var curr: i64 = n;
  if (curr == -9223372036854775808) {
    output[length] = '8';
    ++length;

    curr = -922337203685477580;
  }

  curr = if curr < 0 then -curr else curr;
  while (curr > 0) {
    output[length] = (((curr % 10) + 48) as u8) as char;
    curr /= 10;

    ++length;
  }

  if (n < 0) {
    output[length] = '-';
    ++length;
  } else if (n == 0) {
    output[length] = '0';
    ++length;
  }

  while (length >= 0) {
    Core.PrintChar(output[length]);
    --length;
  }

  Core.PrintChar('\n');
}

fn Run() -> i32 {
  let input: array((i32, i32), 8) = (
    ( 7, 1),
    (11, 1),
    (11, 7),
    ( 9, 7),
    ( 9, 5),
    ( 2, 5),
    ( 2, 3),
    ( 7, 3)
  );

  var best_p1: i64 = 0;
  var best_p2: i64 = 0;
  for (i: i32 in Range(0, k)) {
    let p: (i32, i32) = input[i];
    for (j: i32 in Range(i+1, k)) {
      let q: (i32, i32) = input[j];

      let w: i32 = Abs(q.0 - p.0) + 1;
      let h: i32 = Abs(q.1 - p.1) + 1;

      let area: i64 = (w as i64) * (h as i64);
      if (area <= best_p2) {
        continue;
      }

      if (area > best_p1) {
        best_p1 = area;
      }

      if (IsValidRectangle(input, i, j)) {
        best_p2 = area;
      }
    }
  }

  PrintI64(best_p1);
  PrintI64(best_p2);

  return 0;
}
