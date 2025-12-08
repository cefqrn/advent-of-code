-- https://www.idris-lang.org/pages/example.html
-- https://idris2.readthedocs.io/en/latest/tutorial/index.html
-- https://idris-community.github.io/idris2-tutorial/
-- https://www.idris-lang.org/Idris2/base/
-- https://www.idris-lang.org/Idris2/prelude/
--
-- run with
--   idris2 idris.idr -o idris && build/exec/idris

module Main

import Data.List1
import Data.Vect
import Data.String
import System.File

record JunctionBox where
  constructor MkJunctionBox
  x : Integer
  y : Integer
  z : Integer

components : JunctionBox -> Vect 3 Integer
components (MkJunctionBox x y z) = [x, y, z]

squareDist : Vect n Integer -> Vect n Integer -> Integer
squareDist a b = sum . map (\x => x*x) $ zipWith (-) a b

implementation Show JunctionBox where
  show = joinBy ", " . toList . map show . components

read : String -> Maybe JunctionBox
read s = do
  [x, y, z] <- map (map parseInteger) . toVect 3 . forget . split (== ',') $ s
  [| MkJunctionBox x y z |]

combinations : List a -> List (a, a)
combinations [] = []
combinations (x::xs) = ((,) <$> [x] <*> xs) ++ combinations xs

find : Vect n (Fin n) -> Fin n -> Fin n
find reps i = let j = index i reps in if j == i then i else Main.find reps j

connect : Vect n (Fin n) -> List (Fin n, Fin n) -> Vect n (Fin n)
connect reps []           = map (find reps) reps
connect reps ((i, j)::xs) = connect (replaceAt (find reps i) (find reps j) reps) xs

setSizes : Vect n (Fin n) -> List Nat
setSizes reps = map (\x => count (== x) reps) . nub . toList $ reps

lastConnection : Vect n (Fin n) -> List (Fin n, Fin n) -> Maybe (Fin n, Fin n)
lastConnection _ [] = Nothing
lastConnection reps connections =
  let sizes = setSizes reps in
  let left = pred (length sizes) in
  let (curr, next) = splitAt left connections in
  let reps = connect reps curr in
  if length (setSizes reps) == 1 then last' curr else
    lastConnection reps next

main : IO ()
main = do
  Right input <- readFile "input"
    | Left _  => putStrLn "failed to read input"

  let parseInput = traverse read . lines
  let Just junctionBoxes_ = parseInput input
    | Nothing => putStrLn "failed to parse input"

  let indices = Data.Vect.allFins (length junctionBoxes_)
  let junctionBoxes = Data.Vect.fromList junctionBoxes_

  let connections = combinations $ toList indices

  let squareDistanceBetween = squareDist `on` (components . flip Data.Vect.index junctionBoxes)
  let connections = sortBy (compare `on` uncurry squareDistanceBetween) connections

  let reps = connect indices (take 1000 connections)
  let connections = drop 1000 connections

  let sizes = setSizes reps
  let sizes = sizes |> sort |> reverse

  putStrLn (show (sizes |> take 3 |> product))

  let Just (i, j) = lastConnection reps connections
    | Nothing => putStrLn "couldn't connect all boxes"

  let (MkJunctionBox x1 _ _) = index i junctionBoxes
  let (MkJunctionBox x2 _ _) = index j junctionBoxes

  putStrLn (show (x1 * x2))
