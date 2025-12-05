# https://perldoc.perl.org/perlintro
# https://learn.perl.org/books/beginning-perl/
# https://perldoc.perl.org/perldata
# https://perldoc.perl.org/perlrequick
# https://perldoc.perl.org/perlfunc
# https://perldoc.perl.org/perlop
#
# run with perl perl.pl

use strict;
use warnings;

$, = " ";
$\ = "\n";

open my $input, "<", "input" or die $!;

my @fresh_ranges = ();
while (<$input>) {
  last unless /./;
  die "invalid range" unless /^(\d+)-(\d+)$/;

  push @fresh_ranges, [$1, $2];
}

@fresh_ranges = sort { $a->[0] <=> $b->[0] } @fresh_ranges;

my @merged_ranges = (shift @fresh_ranges);
foreach (@fresh_ranges) {
  my $top = $merged_ranges[-1];
  if ($_->[0] <= $top->[1]) {
    $top->[1] = (sort { $a <=> $b } ($_->[1], $top->[1]))[1];
  } else {
    push @merged_ranges, $_;
  }
}

my $p1 = 0;
while (<$input>) {
  last unless /./;
  die "invalid ingredient" unless /^(\d+)$/;

  $p1 += $_->[0] <= $1 <= $_->[1] foreach @merged_ranges;
}

my $p2 = 0;
$p2 += $_->[1] - $_->[0] + 1 foreach @merged_ranges;

print $p1, $p2;
