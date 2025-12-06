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

let space = char ' '

let eos = function
  | [] -> Some ((), [])
  | _  -> None

let eof =
  maybe newline |>> eos





let rec repeat n =
  if n = 0 then fun _ -> [] else
  let rest = repeat (n-1) in
  fun x -> x :: rest x

let seql ps =
  List.fold_left
    (fun ps p ->
      ps |*> fun rs ->
      p  |*> fun r  ->
        of_value (r::rs))
    (of_value [])
    ps

let exactly n p =
  repeat n p
  |> seql


let digit =
  satisfies (function '0'..'9' -> true | _ -> false)
  |> map (fun c -> (Char.code c) - 48)

let number =
  some digit
  |> map (List.fold_left (fun acc x -> acc*10 + x) 0)



let transpose : 'a list list -> 'a list list = fun l ->
  if List.is_empty l then [] else
  let rec go acc = function
    | []    -> acc
    | x::xs ->
      let acc = List.map2 List.cons x acc in
      go acc xs
  in go (repeat (List.length (List.hd l)) []) l
  |> List.map List.rev



type op = Add | Mul

let number_row =
  some (many space |>> number) <<| many space

let operator =
  char '+' <+> char '*'
  |> map ( function
    | '+' -> Add
    | '*' -> Mul
    | _   -> failwith "impossible" )

let operator_row =
  some (many space |>> operator) <<| many space

let p1_parse =
  separated_by newline number_row |*> fun numbers   ->
  newline                         |>>
  operator_row                    |*> fun operators ->
    of_value (List.combine (transpose numbers) operators)

let lines =
  separated_by newline (some (satisfies (( <> ) '\n')))


let evaluate (nums, o) =
  match o with
  | Add -> List.fold_left ( + ) 0 nums
  | Mul -> List.fold_left ( * ) 1 nums


let stol s = s |> String.to_seq |> List.of_seq

let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol


(* check if the line can be parsed by p *)
let cl_satisfy p = function
  | []      -> None
  | l :: ls -> match p l with
    | Some (x, _) -> Some (x, ls)
    | None -> None

let ()
  = initial_input
  |> p1_parse
  |> ( function
    | None        -> failwith "p1 parsing failed"
    | Some (x, _) -> x )
  |> List.map evaluate
  |> List.fold_left ( + ) 0
  |> Int.to_string
  |> print_endline

  ; initial_input
  |> lines
  |> ( function
    | None        -> failwith "p2 parsing failed: could not split into lines"
    | Some (x, _) -> x )
  |> transpose
  |> separated_by
    (cl_satisfy (some space |>> eos))
    (many (cl_satisfy (
      many space     |>>
      number         |*> fun num ->
      many space     |>>
      maybe operator |*> fun o ->
      eos            |>>
        of_value (num, o))))
  |> ( function
    | None        -> failwith "p2 parsing failed: could not separate expressions"
    | Some (x, _) -> x )
  |> List.map (fun columns ->
    columns
    |> ( function
      | (n, Some o)::xs -> (n :: List.map fst xs, o)
      | _               -> failwith "p2 parsing failed: could not get operator" )
    |> evaluate )
  |> List.fold_left ( + ) 0
  |> Int.to_string
  |> print_endline
