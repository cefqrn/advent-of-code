(* https://stackoverflow.com/a/67221605 *)

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

let maybe p =
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

let stol s = s |> String.to_seq |> List.of_seq
let sum = List.fold_left ( + ) 0


let circuit_box =
  integer  |*> fun x ->
  char ',' |>>
  integer  |*> fun y ->
  char ',' |>>
  integer  |*> fun z ->
    of_value (x, y, z)

let input =
  separated_by newline circuit_box <<| eof

let boxes =
  In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> function
    | None        -> failwith "failed to parse input"
    | Some (x, _) -> Array.of_list x

let rec pairs = function
  | [] -> []
  | x::xs -> List.map (fun y -> (x, y)) xs @ pairs xs

let square_distance (x1, y1, z1) (x2, y2, z2) =
  let dx = x2 - x1 in
  let dy = y2 - y1 in
  let dz = z2 - z1 in
    dx*dx + dy*dy + dz*dz


let rec range start stop =
  if start = stop then [] else
  start :: range (start+1) stop

let reps = ref (Array.of_list (range 0 (Array.length boxes)))

let rec find i =
  let j = Array.get !reps i in
  if i = j then i else
  let rep = find j in
  Array.set !reps i rep;
  rep

let rec union i j =
  let i = find i in
  let j = find j in
  if i = j then false else
    ( Array.set !reps i j; true )

let connections =
  pairs (range 0 (Array.length boxes))
  |> List.sort (fun (a, b) (x, y) ->
    Int.compare
      (square_distance (Array.get boxes a) (Array.get boxes b))
      (square_distance (Array.get boxes x) (Array.get boxes y)))

let left = ref (Array.length boxes - 1)
let rec fully_connect = function
  | [] -> -1
  | (i, j)::xs ->
    if union i j then left := !left - 1;
    if !left > 0 then fully_connect xs else
    let (x1, _, _) = Array.get boxes i in
    let (x2, _, _) = Array.get boxes j in
      x1 * x2

let flip f x y = f y x

let ()
  = connections
  |> List.take 1000
  |> List.iter (fun (i, j) -> if union i j then left := !left - 1)

  ; let counts = Array.make (Array.length boxes) 0 in
  range 0 (Array.length boxes)
  |> List.map find
  |> List.iter (fun i -> Array.set counts i (Array.get counts i + 1))
  ; Array.sort (flip Int.compare) counts
  ; counts
  |> Array.to_list
  |> List.take 3
  |> List.fold_left ( * ) 1
  |> Int.to_string
  |> print_endline

  ; fully_connect (List.drop 1000 connections)
  |> Int.to_string
  |> print_endline
