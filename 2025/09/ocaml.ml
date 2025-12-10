let ( <+> ) p q = fun input ->
  match p input with
  | None -> q input
  | r    -> r

let ( |*> ) p f = fun input ->
  match p input with
  | Some (x, xs) -> f x xs
  | None         -> None

let satisfies p = function
  | x::xs when p x -> Some (x, xs)
  | _              -> None

let of_value x = fun input -> Some (x, input)

let ( |>> ) p q = p |*> fun _ -> q
let ( <<| ) p q = p |*> fun x -> q |*> fun _ -> of_value x



type 'a parser = char list -> ('a * char list) option

let rec many p =
  some p <+> of_value []
and some p =
  p      |*> fun x ->
  many p |*> fun xs ->
    of_value (x::xs)

let separated_by sep p =
  p                |*> fun x ->
  many (sep |>> p) |*> fun xs ->
    of_value (x::xs)

let map f p =
  p |*> fun x -> of_value (f x)

let maybe (p : 'a parser) : 'a option parser =
  map Option.some p <+> of_value None

let digit = satisfies (function '0'..'9' -> true | _ -> false)
let integer =
  map (List.fold_left (fun acc x -> acc * 10 + (Char.code x - 48)) 0) (some digit)

let char c = satisfies (( = ) c)

let cr = char '\r'
let nl = char '\n'
let newline = maybe cr |>> nl

let eos = function
  | [] -> Some ((), [])
  | _  -> None

let eof = maybe newline |>> eos

let comma = char ','
let coordinate : (int * int) parser =
  integer |*> fun x ->
  comma   |>>
  integer |*> fun y ->
    of_value (x, y)


let rec combinations = function
  | []    -> []
  | x::xs -> List.fold_left (fun acc y -> (x, y) :: acc) [] xs @ combinations xs

let pairs = function
  | x::y::xs ->
    ( let rec go = function
      | x::y::xs -> (x, y) :: go (y::xs)
      | _        -> []
      in go (x::y::xs @ [x]) )
  | _ -> []

let bounds ((x1, y1), (x2, y2)) = (min x1 x2, max x1 x2), (min y1 y2, max y1 y2)

let area_of ((x1, y1), (x2, y2)) =
  let dx = abs (x2 - x1) + 1 in
  let dy = abs (y2 - y1) + 1 in
    dx*dy


let coordinates =
  In_channel.stdin
  |> In_channel.input_all
  |> (fun s -> s |> String.to_seq |> List.of_seq)
  |> (separated_by newline coordinate <<| eof)
  |> function
    | None        -> failwith "failed to parse input"
    | Some (x, _) -> x

let walls = pairs coordinates


let validate coords =
  let ((lo_x, hi_x), (lo_y, hi_y)) = bounds coords in
  List.exists (fun wall ->
    let ((x1, x2), (y1, y2)) = bounds wall in
      x1 = x2 && lo_x < x1 && x2 < hi_x && (
           (y1 <= lo_y && lo_y <  y2)
        || (y1 <  hi_y && hi_y <= y2)
        || (lo_y <  y1 && y1 <  hi_y)
        || (lo_y <  y2 && y2 <  hi_y))
      || lo_y < y1 && y2 < hi_y && (
          (x1 <= lo_x && lo_x <  x2)
        || (x1 <  hi_x && hi_x <= x2)
        || (lo_x <  x1 && x1 <  hi_x)
        || (lo_x <  x2 && x2 <  hi_x))) walls
  |> not


let ()
  = combinations coordinates
  |> List.map area_of
  |> List.fold_left max (-1)
  |> Int.to_string
  |> print_endline

  ; combinations coordinates
  |> List.fold_left
    (fun best curr ->
      let area = area_of curr in
      if area <= best then best else
      if validate curr then area else best) (-1)
  |> Int.to_string
  |> print_endline
