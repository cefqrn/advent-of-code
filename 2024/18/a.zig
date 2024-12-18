// https://learnxinyminutes.com/zig/
// https://ziglang.org/learn/overview/
// https://stackoverflow.com/questions/68368122/how-to-read-a-file-in-zig
// https://zig.guide
// https://ziglang.org/documentation/master/
// https://ziglang.org/documentation/master/std/
// https://ziggit.dev/t/how-to-pass-an-array-to-a-function/940/2
//
// run with
//   zig build-exe a.zig && ./a

const std = @import("std");

const Vec2 = struct { x: i8, y: i8 };

const QueueElement = struct {
  score: u32,
  pos: Vec2,
};
const Queue = std.PriorityQueue(QueueElement);

const History = std.HashMap(Vec2, ?Vec2, std.hash_map.AutoContext(Vec2), 80);

const w: i8 = 71;
const h: i8 = 71;

const ipos = Vec2{ .x = 0,   .y = 0   };
const epos = Vec2{ .x = w-1, .y = h-1 };

const InputError = error { InputTooBig };

fn read_input(bytes: []Vec2) !u32 {
  const f = try std.fs.cwd().openFile("input", .{});
  defer f.close();

  var reader = std.io.bufferedReader(f.reader());
  var in_stream = reader.reader();

  var buf: [64]u8 = undefined;
  var byte_count: u32 = 0;
  while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
    if (byte_count == bytes.len)
      return InputError.InputTooBig;

    var it = std.mem.split(line, ",");

    const x = try std.fmt.parseInt(i8, it.next().?, 10);
    const y = try std.fmt.parseInt(i8, it.next().?, 10);

    bytes[byte_count] = Vec2{.x = x, .y = y};
    byte_count += 1;
  }

  return byte_count;
}

fn order_queue_element(a: QueueElement, b: QueueElement) std.math.Order {
  return std.math.order(a.score, b.score);
}

fn in_bounds(pos: Vec2) bool {
  return 0 <= pos.x and pos.x < w
     and 0 <= pos.y and pos.y < h;
}

fn adjacent(pos: Vec2) [4]Vec2 {
  return [4]Vec2{
    Vec2{ .x = pos.x,     .y = pos.y - 1 },
    Vec2{ .x = pos.x + 1, .y = pos.y     },
    Vec2{ .x = pos.x,     .y = pos.y + 1 },
    Vec2{ .x = pos.x - 1, .y = pos.y     }
  };
}

fn reconstruct_path(path: *History, seen: History, pos: Vec2) void {
  var curr = pos;
  path.put(curr, null) catch return;
  while (seen.get(curr).?) |prev| {
    curr = prev;
    path.put(curr, null) catch return;
  }
}

fn get_path(path: *History, fallen: History) bool {
  var left = Queue.init(std.heap.page_allocator, order_queue_element);
  defer left.deinit();

  var seen = History.init(std.heap.page_allocator);
  defer seen.deinit();

  seen.put(ipos, null) catch return false;
  left.add(QueueElement{ .score = 0, .pos = ipos }) catch return false;
  while (left.removeOrNull()) |curr| {
    if (curr.pos.x == epos.x and curr.pos.y == epos.y) {
      reconstruct_path(path, seen, epos);
      return true;
    }

    for (adjacent(curr.pos)) |npos| {
      if (!in_bounds(npos))
        continue;

      if (fallen.contains(npos))
        continue;

      if (seen.contains(npos))
        continue;

      seen.put(npos, curr.pos) catch return false;
      left.add(QueueElement{ .score = curr.score + 1, .pos = npos }) catch return false;
    }
  }

  return false;
}

pub fn main() void {
  var bytes: [4096]Vec2 = undefined;
  const byte_count = read_input(&bytes) catch |err| {
    std.debug.print("failed to read input: {}\n", .{err});
    return;
  };

  var fallen = History.init(std.heap.page_allocator);
  defer fallen.deinit();

  var fallen_count: u32 = 0;
  while (fallen_count < 1024) {
    fallen.put(bytes[fallen_count], null) catch return;
    fallen_count += 1;
  }

  var path = History.init(std.heap.page_allocator);
  defer path.deinit();

  // p1
  if (!get_path(&path, fallen)) {
    std.debug.print("could not find initial path\n", .{});
    return;
  }

  std.debug.print("{}\n", .{path.count() - 1});

  // p2
  while (fallen_count < byte_count) {
    const curr = bytes[fallen_count];

    fallen.put(curr, null) catch return;
    fallen_count += 1;

    if (!path.contains(curr))
      continue;

    path.clearRetainingCapacity();
    if (!get_path(&path, fallen)) {
      std.debug.print("{},{}\n", .{curr.x, curr.y});
      return;
    }
  }

  std.debug.print("path never obstructed\n", .{});
}
