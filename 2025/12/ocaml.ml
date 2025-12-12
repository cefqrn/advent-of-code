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


let sp = char ' '

let tile = char '.' <+> char '#'

let shape =
  integer  |*> fun index ->
  char ':' |>>
  newline  |>>
  separated_by newline (some tile) |*> fun rows ->
    of_value (index, rows)

let region =
  integer  |*> fun width ->
  char 'x' |>>
  integer  |*> fun height ->
  char ':' |>>
  char ' ' |>>
  separated_by sp integer |*> fun amounts ->
    of_value ((width/3) * (height/3) >= sum amounts)

let shapes = separated_by (newline |>> newline) shape
let regions = separated_by newline region

let solve =
  shapes  |*> fun _ ->
  newline |>>
  newline |>>
  regions |*> fun validities ->
    of_value (List.filter (fun x -> x) validities |> List.length)

let () =
  In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> solve
  |> function
    | None             -> print_endline "invalid input"
    | Some (result, _) -> print_endline (Int.to_string result)
