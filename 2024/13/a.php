<?php

/*
  https://learnxinyminutes.com/php/
  https://www.php.net/manual/en/index.php

  run with
    php a.php <input
*/

function solve($px, $py, $ax, $ay, $bx, $by) {
  $b = ($py*$ax - $px*$ay) / ($by*$ax - $bx*$ay);
  $a = ($px - $b*$bx) / $ax;

  // x/y is an integer if both x and y are integers and y divides x (y != 0)
  return is_integer($b) && is_integer($a) ? 3*$a + $b : 0;
}

$p1 = $p2 = 0;
while (true) {
  $success =
  fscanf(STDIN, "Button A: X+%d, Y+%d", $ax, $ay);
  fscanf(STDIN, "Button B: X+%d, Y+%d", $bx, $by);
  fscanf(STDIN, "Prize: X=%d, Y=%d", $px, $py);
  fgets(STDIN);

  if (!$success)
    break;

  $p1 += solve($px, $py, $ax, $ay, $bx, $by);
  $p2 += solve($px + 10000000000000, $py + 10000000000000, $ax, $ay, $bx, $by);
}

echo "$p1\n$p2\n";
