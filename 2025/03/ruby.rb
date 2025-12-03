=begin
  https://ruby-doc.org/
  https://learnxinyminutes.com/ruby/

  run with
    ruby ruby.rb <input
=end

p1 = p2 = 0
readlines(chomp: true).each { |line|
  initial, *rest = line.chars.map &:to_i
  best = [initial]

  rest.each { |joltage|
    best << 0
    [best.length, 12].min.-(2).downto(0) { |i|
      best[i+1] = [best[i+1], best[i]*10 + joltage].max
    }

    best[0] = [best[0], joltage].max
  }

  p1 += best[ 2-1]
  p2 += best[12-1]
}

puts p1, p2
