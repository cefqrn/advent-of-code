#`(
  https://course.raku.org/essentials/
  https://learnxinyminutes.com/raku/

  run with
    raku a.raku
)

my %seen;
class Vec2 {
  has Int $.x;
  has Int $.y;

  multi method new($x, $y) {
    if %seen{$x}{$y} -> $prev {
      return $prev
    }

    my $curr = self.bless(:$x, :$y);
    if %seen{$x} -> %col {
      %col{$y} = $curr
    } else {
      %seen{$x} = {$y => $curr}
    }

    $curr
  }
}

multi prefix:<->(Vec2 $v) {
  Vec2.new(-$v.x, -$v.y)
}

multi infix:<+>(Vec2 $a, Vec2 $b) {
  Vec2.new($a.x + $b.x, $a.y + $b.y)
}

my %directions =
  '^' => Vec2.new( 0, -1),
  '>' => Vec2.new( 1,  0),
  'v' => Vec2.new( 0,  1),
  '<' => Vec2.new(-1,  0);

my %cdirs =
  '[' => %directions{'>'},
  ']' => %directions{'<'};

sub push(SetHash $seen, Vec2 $pos, Vec2 $d, List $grid) returns Bool {
  return True if $seen{$pos};
  $seen.set: $pos;

  my $npos = $pos + $d;
  my $n = $grid[$npos.y][$npos.x];

  return False if $n eq '#';

  if %cdirs{$grid[$pos.y][$pos.x]} -> $cd {
    push($seen, $pos + $cd, $d, $grid) or return False;
  }

  return True if $n eq '.';

  push($seen, $npos, $d, $grid)
}

sub move(SetHash $moved, Vec2 $d, List $igrid) returns List {
  my @ngrid = $igrid>>.Array;

  for $moved.keys -> $ipos {
    my $npos = $ipos + $d;

    @ngrid[$npos.y][$npos.x] = $igrid[$ipos.y][$ipos.x];
    @ngrid[$ipos.y][$ipos.x] = '.' if !$moved{$ipos + -$d};
  }

  @ngrid
}

sub simulate(List $instructions, List $igrid) returns List {
  my $grid = $igrid;

  my ($iy, $ix) = $grid>>.first('@', :k).first(Int, :kv);
  my $pos = Vec2.new($ix, $iy);

  for $instructions.list -> $d {
    my $moved = [].SetHash;
    push($moved, $pos, $d, $grid) or next;

    $pos = $pos + $d;
    $grid = move($moved, $d, $grid);
  }

  $grid
}

my %wide =
  '#' => "##",
  'O' => "[]",
  '@' => "@.",
  '.' => "..";

sub widen(List $grid) returns List {
  $grid>>.&{%wide{$_}}>>.join>>.comb>>.list.list
  #$grid>>.&{%wide{$_}.join.comb.list}.list
}

sub gps-sum(List $grid) returns Int {
  $grid>>.grep(/ <[ O [ ]> /, :k)
    .pairs
    .invert
    .flatmap(*.kv.map: -> $x, $y {100*$y + $x})
    .sum
}


my $f = IO::Path.new("input");

my ($grid-s, $instructions-s) = $f.split("\n\n");

my $igrid = $grid-s.lines>>.comb>>.list;
my $instructions = %directions{$instructions-s.comb(/ <[ > v < ^ ]> /)};

say simulate($instructions, $igrid).&gps-sum;
say simulate($instructions, $igrid.&widen).&gps-sum;

