import Data.Text (pack, splitOn, stripEnd, unpack)
import Data.List (null)
import Data.Set (Set, empty, fromList, insert, member)

parseInput input = parseInput' (map unpack $ splitOn (pack ", ") (stripEnd $ pack input)) []
  where
    parseInput' inp steps
      | null inp  = steps
      | otherwise = (rotation, distance) : parseInput' (tail inp) steps
      where
        rotation = head (head inp) == 'R'
        distance = read (tail $ head inp) :: Integer

p1 parsedInput = p1' parsedInput (0, 0) 0
  where
    p1' inp pos r
      | null inp  = abs (fst pos) + abs (snd pos)
      | otherwise = p1' (tail inp) (if odd newR then (fst pos + (newR - 2) * distance, snd pos) else (fst pos, snd pos + (newR - 1) * distance)) newR
      where
        rotatingRight = fst $ head inp
        distance = snd $ head inp
        newR = mod (if rotatingRight then succ r else pred r) 4

p2 parsedInput = p2' parsedInput (0, 0) 0 0 (fromList [(0, 0)])
  where
    p2' inp pos r d seen
      | r > 0 && member (fst pos - ((d `mod` 2) * (d `mod` 4 - 2)), snd pos - (((d + 1) `mod` 2) * (d `mod` 4 - 1))) seen = fst pos - ((d `mod` 2) * (d `mod` 4 - 2)) + snd pos - (((d + 1) `mod` 2) * (d `mod` 4 - 1))
      | r > 0          = p2' inp (fst pos - ((d `mod` 2) * (d `mod` 4 - 2)), snd pos - (((d + 1) `mod` 2) * (d `mod` 4 - 1))) (r - 1) d (insert (fst pos - ((d `mod` 2) * (d `mod` 4 - 2)), snd pos - (((d + 1) `mod` 2) * (d `mod` 4 - 1))) seen)
      | null inp       = abs (fst pos) + abs (snd pos)
      | fst $ head inp = p2' (tail inp) pos (snd $ head inp) (d + 1) seen
      | otherwise      = p2' (tail inp) pos (snd $ head inp) (d - 1) seen

main = do
  inp <- fmap parseInput getContents
  print (p1 inp)
  print (p2 inp)