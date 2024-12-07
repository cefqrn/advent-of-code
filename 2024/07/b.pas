{
  https://learnxinyminutes.com/docs/pascal
  https://www.taoyue.com/tutorials/pascal
  https://en.wikibooks.org/wiki/Pascal_Programming
  https://www.freepascal.org/docs.var
  https://www.pilotlogic.com/sitejoom/index.php/106-wiki/pascal-basics/chapter-3/145-pascal-pointer-arithmetic.html
  https://www.freepascal.org/docs-html/ref/refse15.html
  https://wiki.freepascal.org/Label

  run with
    fpc a.pas && ./a
  in this directory
}

program pineapple;

type
  arr = array [1..16] of int64;
  arr_p = ^int64;

var
  f: text;
  line: string;
  p1: int64 = 0;
  p2: int64 = 0;

function concat(a, b: int64): int64;
var
  buffer: string;
begin
  writestr(buffer, a, b);
  val(buffer, concat);
end;

function solve(needed: int64; nums: arr_p; count: integer; concat_used: boolean): boolean;
label
  done;
var
  solved: boolean;
  a, b: int64;
begin
  a := nums^;

  if count < 2 then
  begin
    if a <> needed then
      exit(false);

    p2 := p2 + needed;
    if not concat_used then
      p1 := p1 + needed;

    exit(true);
  end;

  inc(nums);
  b := nums^;

  nums^ := a + b;
  solved := solve(needed, nums, count-1, concat_used);
  if solved then
    goto done;

  nums^ := a * b;
  solved := solve(needed, nums, count-1, concat_used);
  if solved then
    goto done;

  nums^ := concat(a, b);
  solved := solve(needed, nums, count-1, true);

done:
  nums^ := b;
  dec(nums);
  exit(solved);
end;

procedure handle_line(line: string);
var
  i, j: integer;
  needed: int64;
  nums: arr;
  count: integer;
begin
  // parse needed
  j := pos(': ', line);
  val(copy(line, 1, j-1), needed);

  // parse nums
  count := 0;

  i := j + 2;
  j := pos(' ', line, i);
  while j <> 0 do
  begin
    count := count + 1;
    val(copy(line, i, j-i), nums[count]);

    i := j + 1;
    j := pos(' ', line, i);
  end;
  count := count + 1;
  val(copy(line, i), nums[count]);

  // solve
  solve(needed, @nums[1], count, false);
end;

begin
  assign(f, 'input'); reset(f);
  while not eoln(f) do
  begin
    readln(f, line);
    handle_line(line);
  end;
  close(f);

  writeln(p1);
  writeln(p2);
end.
