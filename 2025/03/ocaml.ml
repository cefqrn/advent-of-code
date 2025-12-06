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

let ( |>> ) p q =
  p |*> fun _ -> q

let ( <<| ) p q =
  p |*> fun x -> q |*> fun _ -> of_value x


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

let newline = char '\n'

let eos = function
  | [] -> Some ((), [])
  | _  -> None

let eof =
  maybe newline |>> eos

let stol s = s |> String.to_seq |> List.of_seq


let digit =
  satisfies (function '0'..'9' -> true | _ -> false)
  |> map (fun c -> (Char.code c) - 48)

let number =
  some digit
  |> map (List.fold_left (fun acc x -> acc*10 + x) 0)




let join sep = function
  | x::xs -> List.fold_left (fun acc x -> acc ^ sep ^ x) x xs
  | [] -> ""

let list_to_string l =
  "[" ^ join ", " l ^ "]"



let separated_by sep p =
  p                |*> fun x  ->
  many (sep |>> p) |*> fun xs ->
    of_value (x::xs)

let input =
  separated_by newline (some digit) <<| eof

exception ParseError
let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> function
    | Some (x, _) -> x
    | _           -> raise ParseError

let with_joltage best joltage =
  match best with
  | []    -> [joltage]
  | x::xs ->
    List.fold_left
      (fun (curr, rest) best_of_next ->
        ( best_of_next
        , max best_of_next (curr*10 + joltage) :: rest))
      (x, [max x joltage]) xs
    |> fun (last, rest) -> last*10 + joltage :: rest
    |> List.rev

let outputs_at =
  initial_input
  |> List.map (List.fold_left with_joltage [])

let sum =
  List.fold_left ( + ) 0

let ()
  = outputs_at
  |> List.map (fun l -> List.nth l ( 2-1))
  |> sum
  |> Int.to_string
  |> print_endline

  ; outputs_at
  |> List.map (fun l -> List.nth l (12-1))
  |> sum
  |> Int.to_string
  |> print_endline
