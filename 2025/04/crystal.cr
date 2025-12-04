# https://crystal-lang.org/reference/1.18/getting_started/index.html
# https://learnxinyminutes.com/crystal/
# https://crystal-lang.org/reference/1.18/syntax_and_semantics/index.html
# https://stackoverflow.com/a/59494322
# https://docs.ruby-lang.org/en/master/
# https://crystal-lang.org/api/1.18.2/Bool.html
# https://stackoverflow.com/a/58610011

alias VEC2 = {x: Int32, y: Int32}

DIRECTIONS = [
  {x:  0, y:  1}, {x:  1, y:  1},
  {x:  1, y:  0}, {x:  1, y: -1},
  {x:  0, y: -1}, {x: -1, y: -1},
  {x: -1, y:  0}, {x: -1, y:  1}
]

# can't overload VEC2.+
def add(a, b)
  {x: a[:x] + b[:x], y: a[:y] + b[:y]}
end

def adjacent_to(coord)
  DIRECTIONS.map { |direction| add(coord, direction) }
end

Grid = Set(VEC2).new
File.read("input").lines.each_with_index { |line, y|
  line.chars.each_with_index { |c, x|
    Grid << {x: x, y: y} if c == '@'
  }
}

Left = Grid.to_a

def should_remove?(coord)
  adjacent_to(coord).count(&->Grid.includes?(VEC2)) < 4
end

def notify_neighbors(coord)
  adjacent_to(coord).each &->Left.push(VEC2)
end

p1 = Grid.count &->should_remove?(VEC2)
p2 = 0
while !Left.empty?
  next if !Grid.includes? curr = Left.pop
  next if !should_remove? curr
  next if !Grid.delete    curr

  notify_neighbors curr
  p2 += 1
end

puts p1, p2
