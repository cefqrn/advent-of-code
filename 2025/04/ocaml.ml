(*
https://ocaml.org/docs/sets
https://ocaml.org/docs/modules
*)

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


let eos = function
  | [] -> Some ((), [])
  | _  -> None

let eof =
  maybe (char '\n') |>> eos


module Vec2 : sig
  type t = int * int
  val compare : t -> t -> int
end = struct
  type t = int * int
  let compare (px, py) (qx, qy) =
    match Int.compare px qx with
    | 0 -> Int.compare py qy
    | o -> o
end

module Vec2Set = Set.Make(Vec2)


let increment r = fun input ->
  r := !r + 1;
  Some ((), input)

let reset r = fun input ->
  r := 0;
  Some ((), input)

let cx = ref 0
let cy = ref 0

let empty = char '.' |*> fun _ -> of_value []
let paper = char '@' |*> fun _ -> of_value [(!cx, !cy)]

let newline = char '\n' <<| increment cy <<| reset cx
let location = (empty <+> paper) <<| increment cx

let line =
  some location
  |> map List.concat

let input =
  separated_by newline line <<| eof
  |> map List.concat
  |> map Vec2Set.of_list


let stol s = s |> String.to_seq |> List.of_seq

exception ParseError
let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> function
    | Some (x, _) -> x
    | _           -> raise ParseError

let join sep = function
  | x::xs -> List.fold_left (fun acc x -> acc ^ sep ^ x) x xs
  | [] -> ""

let list_to_string l = "[" ^ join ", " l ^ "]"


let neighbors_of (x, y) =
  [ (x+0, y+1); (x+1, y+1)
  ; (x+1, y+0); (x+1, y-1)
  ; (x+0, y-1); (x-1, y-1)
  ; (x-1, y+0); (x-1, y+1) ]

let should_remove_from grid c =
  neighbors_of c
  |> List.filter (fun neighbor -> Vec2Set.mem neighbor grid)
  |> List.length
  |> fun amount -> amount < 4

let remove_all_possible grid =
  let rec go acc grid =
    let removing = grid |> Vec2Set.filter (should_remove_from grid) in
    if Vec2Set.is_empty removing then acc else

    let new_grid = Vec2Set.diff grid removing in
    go (acc + Vec2Set.cardinal removing) new_grid
  in go 0 grid


let ()
  = initial_input
  |> Vec2Set.filter (should_remove_from initial_input)
  |> Vec2Set.cardinal
  |> Int.to_string
  |> print_endline

  ; initial_input
  |> remove_all_possible
  |> Int.to_string
  |> print_endline
