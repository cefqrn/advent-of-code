{-
  https://pursuit.purescript.org/
  https://github.com/purescript/documentation/blob/master/guides/Getting-Started.md
  https://github.com/purescript/documentation/blob/master/language/Differences-from-Haskell.md
  https://stackoverflow.com/questions/35705155/how-to-read-a-file-in-purescript-readfile
  https://stackoverflow.com/questions/51158098/how-do-i-convert-a-string-to-a-list-of-chars-in-purescript
  https://stackoverflow.com/questions/65698897/how-to-change-the-node-stack-limit-for-spago

  run with
    spago build && node --stack-size=999999 -e 'import { main } from "./output/Main/index.js"; main()'
-}

module Main where

import Prelude

import Control.Alternative (guard)
import Data.Foldable (sum)
import Data.List (List(Nil), fromFoldable, head, length, sort, zipWith, (:))
import Data.Map (Map, delete, isEmpty, keys, lookup)
import Data.Map as M  -- empty, insert
import Data.Maybe (fromJust)
import Data.Set (Set, member, size, union)
import Data.Set as S  -- empty, insert
import Data.String.CodeUnits (toCharArray)
import Data.Tuple.Nested ((/\))
import Effect (Effect)
import Effect.Console (log)
import Node.FS.Sync (readTextFile)
import Node.Encoding (Encoding(UTF8))
import Partial.Unsafe (unsafePartial)

type Position =
  { x :: Int
  , y :: Int
  }

type Displacement =
  { x :: Int
  , y :: Int
  }

type Grid = Map Position Char
type Region = Set Position

directions :: List Displacement
directions = fromFoldable
  [ { x:  0, y: -1 }  -- up
  , { x:  1, y:  0 }  -- right
  , { x:  0, y:  1 }  -- down
  , { x: -1, y:  0 }  -- left
  ]

right :: Displacement -> Displacement
right d
  | d == {x:  0, y: -1} = {x:  1, y:  0}
  | d == {x:  1, y:  0} = {x:  0, y:  1}
  | d == {x:  0, y:  1} = {x: -1, y:  0}
  | otherwise           = {x:  0, y: -1}

left :: Displacement -> Displacement
left = right <<< right <<< right

grid :: List Char -> Grid
grid s = grid' s 0 0
  where
    grid' Nil _ _ = M.empty
    grid' (c:xs) x y
      | c == '\n' = grid' xs 0 (y + 1)
      | otherwise = let g = grid' xs (x + 1) y in M.insert { x, y } c g

region :: Grid -> Position -> Region
region ig ip = S.insert ip $ region' (delete ip ig) ip directions
  where
    c = lookup ip ig
    region' _ _ Nil = S.empty
    region' g p (d:ds)
      | lookup (p+d) g /= c = region' g p ds
      | otherwise = let r = region g (p+d) in
          union r (region' (difference r g) p ds)

peek :: Grid -> Position
peek s = unsafePartial (fromJust <<< head <<< fromFoldable $ keys s)

difference :: Region -> Grid -> Grid
difference r m = difference' (fromFoldable r) m
  where
    difference' Nil m' = m'
    difference' (x:xs) m' = difference' xs (delete x m')

regions :: Grid -> List Region
regions g
  | isEmpty g = Nil
  | otherwise = let r = region g (peek g) in
      r : regions (difference r g)

area :: Region -> Int
area = size

perimeter :: Region -> Int
perimeter r = length do
  p <- fromFoldable r
  d <- directions
  guard $ not (member (p + d) r)
  pure p

sideCount :: Region -> Int
sideCount r = sideCount' (sort $ fromFoldable r) directions S.empty
  where
    sideCount' Nil _ _ = 0
    sideCount' (_:ps) Nil seen = sideCount' ps directions seen
    sideCount' (p:ps) (d:ds) seen
      | member (p+d) r                   = sideCount' (p:ps) ds seen
      | member (d /\ (p + right d)) seen = sideCount' (p:ps) ds (S.insert (d /\ p) seen)
      | member (d /\ (p + left  d)) seen = sideCount' (p:ps) ds (S.insert (d /\ p) seen)
      | otherwise                        = sideCount' (p:ps) ds (S.insert (d /\ p) seen) + 1

p1 :: List Region -> Int
p1 r = sum $ zipWith (*) (map area r) (map perimeter r)

p2 :: List Region -> Int
p2 r = sum $ zipWith (*) (map area r) (map sideCount r)

main :: Effect Unit
main = do
  contents <- readTextFile UTF8 "input"
  let rs = regions <<< grid <<< fromFoldable <<< toCharArray $ contents

  log <<< show $ p1 rs
  log <<< show $ p2 rs
