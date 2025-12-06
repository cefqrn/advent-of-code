let ( |*> ) p f = fun input ->
  match p input with
  | Some (x, xs) -> f x xs
  | None         -> None

let alt p q = fun input ->
  match p input with
  | None -> q input
  | r    -> r

let of_value x = fun input -> Some (x, input)

let rec many p =
  alt (some p) (of_value [])
and some p =
  p      |*> fun x ->
  many p |*> fun xs ->
    of_value (x::xs)

let map f p =
  p |*> fun x ->
    of_value (f x)

let maybe p =
  alt (map Option.some p) (of_value None)

let never = fun _ -> None

let satisfies p = function
  | x::xs when p x -> Some (x, xs)
  | _              -> None

let char c = satisfies (( = ) c)

let rec string s =
  match s with
  | c::cs ->
    char c    |*> fun _ ->
    string cs |*> fun _ ->
      of_value s
  | [] -> of_value []

let eof = function
  | [] -> Some ((), [])
  | _  -> None

let stol s = s |> String.to_seq |> List.of_seq

let comma   = char ','
let hyphen  = char '-'
let newline = char '\n'

let digit =
  satisfies (function '0'..'9' -> true | _ -> false)
  |> map (fun c -> (Char.code c) - 48)

let number =
  some digit
  |> map (List.fold_left (fun acc x -> acc*10 + x) 0)

let range =
  number |*> fun start ->
  hyphen |*> fun _     ->
  number |*> fun stop  ->
    of_value (start, stop)

let input =
  range |*> fun r ->
  ( many
    ( comma |*> fun _ ->
      range |*> fun r ->
        of_value r)) |*> fun rs ->
  maybe newline |*> fun _ ->
  eof           |*> fun _ ->
    of_value (r::rs)


(* not including empty string *)
let rec substrings = function
  | x::xs -> [x] :: List.map (fun r -> x::r) (substrings xs)
  | []    -> []

let matches predicate s =
  s
  |> Int.to_string
  |> stol
  |> predicate

let matcher f = fun s ->
  substrings s
  |> List.map string
  |> List.map f
  |> List.fold_left alt never
  |> fun p -> p s
  |> Option.is_some

let invalid_p1 =
  matcher (fun p ->
    p   |*> fun _ ->
    p   |*> fun _ ->
    eof |*> fun _ ->
      of_value ())

let invalid_p2 =
  matcher (fun p ->
    p      |*> fun _ ->
    some p |*> fun _ ->
    eof    |*> fun _ ->
      of_value ())

let expand (start, stop) =
  let rec go acc n =
    let acc = n :: acc in
    if n = stop then acc else
      go acc (n+1) in
  go [] start

exception ParseError
let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> function
    | Some (x, _) -> x
    | _           -> raise ParseError

let expanded_input
  = initial_input
  |> List.map expand
  |> List.concat

let sum = List.fold_left ( + ) 0

let _
  = expanded_input
  |> List.filter (matches invalid_p1)
  |> sum
  |> Int.to_string
  |> print_endline

  ; expanded_input
  |> List.filter (matches invalid_p2)
  |> sum
  |> Int.to_string
  |> print_endline
