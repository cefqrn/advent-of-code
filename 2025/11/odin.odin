// https://odin-lang.org/docs/overview/
// https://learnxinyminutes.com/odin/
// https://forum.odin-lang.org/t/using-a-map-after-delete-delete-vs-clear-map/547/5
//
// run with
//   odin run odin.odin -file -sanitize:address

package main

import "core:fmt"
import "core:os"
import "core:strings"

count_paths :: proc(source: string, destination: string, outputs_of: map[string][dynamic]string, cache: ^map[string]int) -> int {
  if source == destination {
    return 1
  }

  cache_key := strings.concatenate({source, destination})

  cached, in_cache := cache^[cache_key]
  if in_cache {
    delete(cache_key)
    return cached
  }

  result := 0
  outputs, has_outputs := outputs_of[source]
  if has_outputs {
    for output in outputs_of[source] {
      result += count_paths(output, destination, outputs_of, cache)
    }
  }

  cache^[cache_key] = result

  return result
}

main :: proc() {
  // parse inputs
  data, success := os.read_entire_file_from_filename("input")
  if !success {
    fmt.println("couldn't read input")
    return
  }

  input := strings.clone_from_bytes(data)
  defer delete(input)
  delete(data)

  outputs_of := make(map[string][dynamic]string)
  defer delete(outputs_of)

  lines := strings.split_lines(strings.trim_right_space(input))
  for line in lines {
    ss := strings.split(line, ": ")
    defer delete(ss)

    outputs := strings.split(ss[1], " ")
    defer delete(outputs)

    source := ss[0]
    outputs_of[source] = make([dynamic]string)
    for output in outputs {
      append(&outputs_of[source], output)
    }
  }
  delete(lines)

  // solve
  cache := make(map[string]int)
  defer delete(cache)

  p1 := count_paths("you", "out", outputs_of, &cache)
  p2 := count_paths("svr", "dac", outputs_of, &cache) \
      * count_paths("dac", "fft", outputs_of, &cache) \
      * count_paths("fft", "out", outputs_of, &cache) \
      + count_paths("svr", "fft", outputs_of, &cache) \
      * count_paths("fft", "dac", outputs_of, &cache) \
      * count_paths("dac", "out", outputs_of, &cache)

  fmt.println(p1, p2)

  // count_paths allocates cache keys
  for k, _ in cache {
    delete(k)
  }

  for _, v in outputs_of {
    delete(v)
  }
}
