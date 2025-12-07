//! https://learnxinyminutes.com/zig/
//! https://ziglang.org/learn/overview/
//! https://ziglang.org/learn/samples/
//! https://ziglang.org/documentation/master/
//! https://stackoverflow.com/a/79746243
//!
//! run with
//!   zig build-exe zig.zig && ./zig

const std = @import("std");

pub fn main() !void {
  const input_file = try std.fs.cwd().openFile("input", .{});
  defer input_file.close();

  var buf = [_]u8{0} ** 256;
  var file_reader = input_file.reader(&buf);
  const reader = &file_reader.interface;

  var beams = [_]usize{0} ** 256;
  {
    const first_line = (try reader.takeDelimiter('\n')).?;
    const initial_beam_index = std.mem.indexOfScalar(u8, first_line, 'S').?;
    beams[initial_beam_index] = 1;
  }

  var p1: usize = 0;
  while (try reader.takeDelimiter('\n')) |line| {
    const lineLength = line.len;

    var new_beams = [_]usize{0} ** 256;

    if (line[0           ] != '^') new_beams[0           ] += beams[0           ];
    if (line[lineLength-1] != '^') new_beams[lineLength-1] += beams[lineLength-1];
    for (1..lineLength-1, line[1..lineLength-1], beams[1..lineLength-1]) |i, c, beam_count| {
      if (c == '^') {
        if (beam_count > 0)
          p1 += 1;

        new_beams[i+1] += beam_count;
        new_beams[i-1] += beam_count;
      } else {
        new_beams[i] += beam_count;
      }
    }

    beams = new_beams;
  }

  var p2: usize = 0;
  for (beams) |beam_count|
    p2 += beam_count;

  try std.fs.File.stdout().writeAll(
    try std.fmt.bufPrint(&buf, "{} {}\n", .{p1, p2}));
}
