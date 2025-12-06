let ( |*> ) p f = fun input ->
  match p input with
  | Some (x, xs) -> f x xs
  | _            -> None

let alt p q = fun input ->
  match p input with
  | None   -> q input
  | result -> result

let of_value x =
  fun input -> Some (x, input)

let map f p = p |*> fun x -> of_value (f x)

let rec many p =
  alt (some p) (of_value [])
and some p =
  p      |*> fun x  ->
  many p |*> fun xs ->
    of_value (x :: xs)

let maybe p =
  alt (map (fun r -> Some r) p) (of_value None)


let satisfies p = function
  | x::xs when p x -> Some (x, xs)
  | _              -> None

let char c = satisfies (( = ) c)

let digit =
  satisfies (function '0'..'9' -> true | _ -> false)
  |> map (fun c -> (Char.code c) - 48)

let number =
  some digit
  |> map (List.fold_left (fun acc b -> acc*10 + b) 0)

let eof = function
  | [] -> Some ((), [])
  | _  -> None


let stol s = s |> String.to_seq |> List.of_seq


let rotation =
  alt (char 'L') (char 'R') |*> fun d ->
  number                    |*> fun n ->
    of_value (if d = 'R' then n else -n)

let line =
  rotation          |*> fun r ->
  maybe (char '\n') |*> fun _ ->
    of_value r

let input =
  many line |*> fun result ->
  eof       |*> fun _      ->
    of_value result


let p1 l =
  List.fold_left
    ( fun (result, current_rotation) rotation ->
      let new_rotation =
        current_rotation + rotation in
      let new_result =
        if new_rotation mod 100 = 0 then result + 1 else result in
      (new_result, new_rotation) )
    (0, 50) l
  |> fst

let rec repeat n =
  if n = 0 then fun _ -> [] else
  let rest = repeat (n-1) in
    fun x -> x :: rest x

let p2_transform n =
  let sign = if n < 0 then -1 else 1 in
    repeat (n*sign) sign


let initial_input
  = In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> Option.get
  |> fst

let _
  = initial_input
  |> p1
  |> Int.to_string
  |> print_endline

  ; initial_input
  |> List.map p2_transform
  |> List.concat
  |> p1
  |> Int.to_string
  |> print_endline
