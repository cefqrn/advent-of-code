import Data.List (transpose, reverse, intercalate, sortBy)

rotate = transpose . reverse

count c a = length (filter (== c) a)

calculateLoad a =
  sum (zipWith (*) [1..] (map (count 'O') (reverse a)))

showArray = intercalate "\n"

-- splitOn =
--   splitOn' [""]
--   where
--     splitOn' l c "" = l
--     splitOn' l c (s:ss) =
--       if s == c
--       then splitOn' (l ++ [""]) c ss
--       else splitOn' (init l ++ [last l ++ [s]]) c ss

splitOn c = foldr (\x (s:ss) -> if x == c then "":s:ss else (x:s):ss) [""]

sections = splitOn '#'

unsections = intercalate "#"

tilt =
  transpose . map fallColumn . transpose
  where
    fallColumn c = unsections (map (sortBy compareRock) (sections c))

spinCycle = rotate . tilt . rotate . tilt . rotate . tilt . rotate . tilt

compareRock a b
  | a == b = EQ
  | a == '.' = GT
  | otherwise = LT

p2 platform =
  p2' [platform] platform
  where
    p2' seen platform
      | next `elem` seen = length seen
      | otherwise = p2' (next : seen) next
      where
        next = spinCycle platform

findCycle l =
  findCycle' l l 1
  where
    findCycle' tortoise hare cycleLength
      | ntortoise == nhare = (ntortoise, cycleLength)
      | otherwise = findCycle' ntortoise nhare (cycleLength + 1)
      where
        ntortoise = spinCycle tortoise
        nhare = spinCycle (spinCycle hare)

main = do
  platform <- fmap lines getContents
  print (calculateLoad (tilt platform))
  let (tortoise, cycleLengthMultiple) = findCycle platform
  print (calculateLoad (iterate spinCycle tortoise !! ((1000000000 - cycleLengthMultiple) `mod` cycleLengthMultiple)))
