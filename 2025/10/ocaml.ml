(*
https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
https://ocaml.org/docs/maps
*)

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


let surrounded_by prefix suffix p = prefix |>> p <<| suffix

let light =
  (char '.' |> map (fun _ -> false)) <+> (char '#' |> map (fun _ -> true))
let diagram =
  surrounded_by (char '[') (char ']') (some light)

let button =
  surrounded_by (char '(') (char ')') (separated_by (char ',') integer)

let joltages =
  surrounded_by (char '{') (char '}') (separated_by (char ',') integer)

let machine =
  diagram  |*> fun d ->
  char ' ' |>>
  separated_by (char ' ') button |*> fun b ->
  char ' ' |>>
  joltages |*> fun j ->
    of_value (d, b, j)

let input = separated_by newline machine

let rec combinations size p =
  if size == 0 then [[]] else
  match p with
  | []    -> []
  | x::xs ->
    List.map (List.cons x) (combinations (size-1) xs) @ combinations size xs

let rec range start stop =
  if start = stop then [] else
    start :: range (start+1) stop

module CacheKey = struct
  type t = bool list * int list list
  let compare (d1, b1) (d2, b2) =
    match List.compare Bool.compare d1 d2 with
    | 0 -> List.compare (List.compare Int.compare) b1 b2
    | o -> o
end

module Cache = Map.Make(CacheKey)

let cache = ref Cache.empty

let flip f x y = f y x

let light_configuration_possibilities initial_diagram buttons =
  match Cache.find_opt (initial_diagram, buttons) !cache with
  | Some cached_value -> cached_value
  | None ->
    let diagram = Array.of_list initial_diagram in
    let result =
      range 0 (List.length buttons + 1)
      |> List.concat_map (flip combinations buttons)
      |> List.filter_map ( fun buttons ->
        buttons
        |> List.iter (List.iter (fun i -> Array.set diagram i (not (Array.get diagram i))));

        let is_valid = Array.for_all (fun x -> not x) diagram in

        buttons
        |> List.iter (List.iter (fun i -> Array.set diagram i (not (Array.get diagram i))));

        if is_valid then Some buttons else None ) in

    cache := Cache.add (initial_diagram, buttons) result !cache;
    result

(* max_int might overflow *)
let inf = 99999

let is_odd x = x mod 2 = 1
let rec joltage_configuration_cost joltages buttons =
  if List.for_all (fun x -> x = 0) joltages then 0 else

  let bits = List.map is_odd joltages in
  light_configuration_possibilities bits buttons
  |> List.map ( fun buttons_pushed ->
    let joltages = Array.of_list joltages in
    buttons_pushed
    |> List.concat
    |> List.iter (fun i -> Array.set joltages i (Array.get joltages i - 1));

    if Array.exists (fun x -> x < 0) joltages then inf else

    let joltages =
      joltages
      |> Array.to_list
      |> List.map (fun x -> x / 2) in

    List.length buttons_pushed + 2 * joltage_configuration_cost joltages buttons )
  |> List.fold_left min inf


let machines =
  In_channel.stdin
  |> In_channel.input_all
  |> stol
  |> input
  |> function
    | None        -> failwith "failed to parse input"
    | Some (x, _) -> x

let ()
  = machines
  |> List.map (fun (diagram, buttons, _) -> light_configuration_possibilities diagram buttons)
  |> List.map (List.map List.length)
  |> List.map (List.fold_left min inf)
  |> sum
  |> Int.to_string
  |> print_endline

  ; machines
  |> List.map (fun (_, buttons, joltages) -> joltage_configuration_cost joltages buttons)
  |> sum
  |> Int.to_string
  |> print_endline
