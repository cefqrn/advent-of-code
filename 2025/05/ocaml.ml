let ( <+> ) p q = fun input ->
  match p input with
  | None -> q input
  | r    -> r

let ( |*> ) p f = fun input ->
  match p input with
  | Some (x, input) -> f x input
  | None            -> None

let of_value x = fun input -> Some (x, input)

let ( |>> ) p q = p |*> fun _ -> q
let ( <<| ) p q = p |*> fun x -> q |*> fun _ -> of_value x

let rec many p =
  some p <+> of_value []
and some p =
  p      |*> fun x ->
  many p |*> fun xs ->
    of_value (x::xs)

let maybe p =
  ( <+> )
    (p |*> fun x -> of_value (Some x))
    (of_value None)

let separated_by sep p =
  p                |*> fun x  ->
  many (sep |>> p) |*> fun xs ->
    of_value (x::xs)


let map f p = p |*> fun x -> of_value (f x)


let satisfies p = function
  | x::xs when p x -> Some (x, xs)
  | _              -> None

let char c = satisfies (( = ) c)


let newline =
  maybe (char '\r') |>> char '\n'

let eos = function
  | [] -> Some ((), [])
  | _  -> None

let eof =
  maybe newline |>> eos


let digit =
  satisfies (function '0'..'9' -> true | _ -> false)
  |> map (fun c -> (Char.code c) - 48)

let number =
  some digit
  |> map (List.fold_left (fun acc x -> acc*10 + x) 0)



let range =
  number   |*> fun lo ->
  char '-' |>>
  number   |*> fun hi ->
    of_value (lo, hi)

let ranges =
  separated_by newline range

let ingredients =
  separated_by newline number

let input =
  ranges      |*> fun r ->
  newline     |>>
  newline     |>>
  ingredients |*> fun i ->
    of_value (r, i)


let stol s = s |> String.to_seq |> List.of_seq

exception ParseError
let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> (input <<| eof)
  |> function
    | Some (x, _) -> x
    | _           -> raise ParseError

let sum = List.fold_left ( + ) 0


let merged ranges =
  ranges
  |> List.sort compare
  |> List.fold_left
    ( fun acc (lo1, hi1) ->
      match acc with
      | (lo2, hi2)::xs when lo1 <= hi2 -> (lo2, max hi1 hi2)::xs
      | _                              -> (lo1, hi1)::acc )
    []

let range_size (lo, hi) = hi - lo + 1
let range_contains n (lo, hi) = lo <= n && n <= hi

let (merged_ranges, ingredients)
  = merged (fst initial_input), snd initial_input

let ()
  = ingredients
  |> List.filter (fun n -> List.exists (range_contains n) merged_ranges)
  |> List.length
  |> Int.to_string
  |> print_endline

  ; merged_ranges
  |> List.map range_size
  |> sum
  |> Int.to_string
  |> print_endline
