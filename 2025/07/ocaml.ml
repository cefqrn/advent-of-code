let ()
  = In_channel.stdin
  |> In_channel.input_lines
  |> List.map (fun s -> s |> String.to_seq |> List.of_seq)
  |> ( function
    | []    -> (0, 0)
    | first_line::xs ->
      let beams = List.map (function 'S' -> 1 | _ -> 0) first_line in
      List.fold_left
        ( fun (p1, beams) line ->
          List.fold_left
            ( fun (p1_diff, new_beams) ((x, c), ((lx, lc), (rx, rc))) ->
              let p1_diff = p1_diff + if c = '^' && x > 0 then 1 else 0 in
              let nx =      if  c <> '^' then  x else 0 in
              let nx = nx + if lc  = '^' then lx else 0 in
              let nx = nx + if rc  = '^' then rx else 0 in
              (p1_diff, nx::new_beams) )
            (0, [])
            (List.combine
              (List.combine
                (0::beams @ [0])
                ('.'::line @ ['.']))
              (List.combine
                (List.combine
                  (0::0::beams)
                  ('.'::'.'::line))
                (List.combine
                  (beams @ [0; 0])
                  (line @ ['.'; '.']))))
          |> fun (p1_diff, new_beams) -> (p1 + p1_diff, List.tl (List.rev (List.tl new_beams))) )
        (0, beams) xs
      |> fun (p1, beams) -> (p1, (List.fold_left ( + ) 0 beams)) )
  |> fun (p1, p2) -> print_endline (Int.to_string p1 ^ " " ^ Int.to_string p2)
