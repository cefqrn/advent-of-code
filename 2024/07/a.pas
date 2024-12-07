{
  https://learnxinyminutes.com/docs/pascal
  https://www.taoyue.com/tutorials/pascal
  https://en.wikibooks.org/wiki/Pascal_Programming
  https://www.freepascal.org/docs.var

  run with
    fpc a.pas && ./a
  in this directory
}

program pineapple;

type
  arr = array [1..16] of int64;

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

function solve(concat_used: boolean; needed: int64; nums: arr; count: integer): boolean;
var
  i: integer;
  new_nums: arr;
begin
  if count < 2 then
  begin
    if nums[1] <> needed then
      exit(false);

    p2 := p2 + needed;
    if not concat_used then
      p1 := p1 + needed;

    exit(true);
  end;

  for i := 3 to count do
    new_nums[i-1] := nums[i];

  new_nums[1] := nums[1] + nums[2];
  if solve(concat_used, needed, new_nums, count-1) then
    exit(true);

  new_nums[1] := nums[1] * nums[2];
  if solve(concat_used, needed, new_nums, count-1) then
    exit(true);

  new_nums[1] := concat(nums[1], nums[2]);
  if solve(true, needed, new_nums, count-1) then
    exit(true);

  exit(false);
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
  solve(false, needed, nums, count);
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
