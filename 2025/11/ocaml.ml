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


let any = satisfies (fun _ -> true)

let ltos l = l |> List.to_seq |> String.of_seq

let device_name =
  any |*> fun a ->
  any |*> fun b ->
  any |*> fun c ->
    of_value (ltos [a; b; c])

let device =
  device_name |*> fun name ->
  char ':'    |>>
  char ' '    |>>
  separated_by (char ' ') device_name |*> fun outputs ->
    of_value (name, outputs)

module StringMap = Map.Make(String)

let outputs_of =
  In_channel.stdin
  |> In_channel.input_all
  |> (fun s -> s |> String.to_seq |> List.of_seq)
  |> (separated_by newline device <<| eof)
  |> ( function
    | None        -> failwith "failed to parse input"
    | Some (x, _) -> x )
  |> List.fold_left (fun map (name, outputs) -> StringMap.add name outputs map) StringMap.empty

let cache = ref StringMap.empty

let rec count_paths_to destination source =
  if source = destination then 1 else
  let cache_key = source ^ destination in
  match StringMap.find_opt cache_key !cache with
  | Some cached_value -> cached_value
  | None ->
    let result =
      match StringMap.find_opt source outputs_of with
      | None -> 0
      | Some outputs ->
        outputs
        |> List.map (count_paths_to destination)
        |> List.fold_left ( + ) 0 in
    cache := StringMap.add cache_key result !cache;
    result

let ()
  = count_paths_to "out" "you"
  |> Int.to_string
  |> print_endline

  ; count_paths_to "out" "fft"
  * count_paths_to "fft" "dac"
  * count_paths_to "dac" "svr"
  + count_paths_to "out" "dac"
  * count_paths_to "dac" "fft"
  * count_paths_to "fft" "svr"
  |> Int.to_string
  |> print_endline
