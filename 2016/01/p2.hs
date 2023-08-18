import Data.Text (pack, splitOn, stripEnd, unpack)
import Data.List (null)
import Data.Set (empty, insert, member)

parseInput input = parseInput' (map unpack $ splitOn (pack ", ") (stripEnd $ pack input)) []
  where
    parseInput' inp steps
      | null inp  = steps
      | otherwise = (rotation, distance) : parseInput' (tail inp) steps
      where
        (r:d) = head inp
        rotation = r == 'R'
        distance = read d :: Integer

p1 parsedInput = p1' parsedInput (0, 0) 0
  where
    p1' input position rotation
      | null input      = abs x + abs y
      | odd newRotation = p1' (tail input) (x + (newRotation - 2) * distance, y) newRotation
      | otherwise       = p1' (tail input) (x, y + (newRotation - 1) * distance) newRotation
      where
        (x, y) = position
        (rotatingRight, distance) = head input
        newRotation = mod (if rotatingRight then rotation + 1 else rotation - 1) 4

p2 parsedInput = p2' parsedInput (0, 0) 0 0 empty
  where
    p2' input position distance rotation seen
      | distance < 1         = if null input then error "never revisited a location" else p2' (tail input) position newDistance newRotation seen
      | member position seen = abs x + abs y
      | otherwise            = p2' input newPosition (distance - 1) rotation (insert position seen)
      where
        (x, y) = position
        (rotatingRight, newDistance) = head input
        newRotation = mod (if rotatingRight then rotation + 1 else rotation - 1) 4
        newPosition = (x - ((rotation `mod` 2) * (rotation - 2)), y - (((rotation + 1) `mod` 2) * (rotation - 1)))

main = do
  inp <- fmap parseInput getContents
  print (p1 inp)
  print (p2 inp)
