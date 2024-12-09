import gleam/bool
import gleam/erlang
import gleam/int
import gleam/io
import gleam/list
import gleam/string

type File {File(
  position: Int,
  length: Int,
  id: Int
)}

type Free {Free(
  position: Int,
  length: Int
)}

type Disk {Disk(
  files: List(File),
  free: List(Free)
)}

pub fn main() {
  case erlang.get_line("") {
    Error(_) -> io.println("no input")
    Ok(input) -> {
      let disk = parse(input)
      let Disk(files, free) = disk

      // p1
      files
      |> list.map(split_file)
      |> list.flatten
      |> Disk(free)
      |> reorder
      |> checksum
      |> int.to_string
      |> io.println

      // p2
      disk
      |> reorder
      |> checksum
      |> int.to_string
      |> io.println
    }
  }
}

fn parse_inner(input: String, position: Int, file_id: Int, is_file: Bool) -> Disk {
  case string.pop_grapheme(input) {
    Ok(#("\n", "")) | Error(_) -> Disk([], [])
    Ok(#(c, rest)) -> case int.parse(c) {
      Error(_) -> panic
      Ok(n) -> {
        let Disk(files, free) = parse_inner(rest, position + n, file_id + bool.to_int(is_file), !is_file)
        case is_file {
          True -> Disk([File(position, n, file_id), ..files], free)
          False if n > 0 -> Disk(files, [Free(position, n), ..free])
          False -> Disk(files, free)
        }
      }
    }
  }
}

fn parse(input: String) -> Disk {
  parse_inner(input, 0, 0, True)
}

fn first_match(list: List(value), predicate: fn(value) -> Bool) -> Result(#(List(value), value, List(value)), Nil) {
  case list {
    [] -> Error(Nil)
    [c, ..rest] -> {
      case predicate(c) {
        True -> Ok(#([], c, rest))
        False -> case first_match(rest, predicate) {
          Error(_) -> Error(Nil)
          Ok(#(before, v, after)) -> Ok(#([c, ..before], v, after))
        }
      }
    }
  }
}

fn reorder_inner(disk: Disk) -> Disk {
  // doesn't free the space previously used by a file
  case disk {
    Disk([], _) | Disk(_, []) -> disk
    Disk(files, free) -> {
      let assert [curr_file, ..rest_files] = files
      let File(file_position, used, id) = curr_file

      case first_match(free, fn(space) {let Free(_, available) = space available >= used}) {
        // not enough space
        Error(_) -> {
          let Disk(new_rest_files, new_free) = reorder_inner(Disk(rest_files, free))
          Disk([curr_file, ..new_rest_files], new_free)
        }
        // free space located after the file (can't use guard on only one side so code repeated)
        Ok(#(_, Free(position, _), _)) if file_position < position -> {
          let Disk(new_rest_files, new_free) = reorder_inner(Disk(rest_files, free))
          Disk([curr_file, ..new_rest_files], new_free)
        }
        // file fully takes up free space
        Ok(#(free_before, Free(position, available), free_after)) if used == available -> {
          let Disk(new_rest_files, new_free) = reorder_inner(Disk(rest_files,
            list.flatten([free_before, free_after])))

          Disk([File(position, used, id), ..new_rest_files], new_free)
        }
        // file doesn't fully take up free space
        Ok(#(free_before, Free(position, available), free_after)) -> {
          let Disk(new_rest_files, new_free) = reorder_inner(Disk(rest_files,
            list.flatten([
              free_before,
              list.wrap(Free(position + used, available - used)),
              free_after])))

          Disk([File(position, used, id), ..new_rest_files], new_free)
        }
      }
    }
  }
}

fn reorder(disk: Disk) -> Disk {
  // assumes files are sorted by position
  let Disk(files, free) = disk
  reorder_inner(Disk(list.reverse(files), free))
}

fn file_checksum(file: File) -> Int {
  case file {
    File(_, 0, _) -> 0
    // File(position, used, id) -> position*id + file_checksum(File(position+1, used-1, id))
    File(position, used, id) -> id * {used*{position-1} + used*{used+1}/2}
  }
}

fn checksum(disk: Disk) -> Int {
  disk.files
  |> list.map(file_checksum)
  |> int.sum
}

fn split_file(file: File) -> List(File) {
  case file {
    File(_, 0, _) -> []
    File(position, length, id) -> [File(position, 1, id), ..split_file(File(position+1, length-1, id))]
  }
}
