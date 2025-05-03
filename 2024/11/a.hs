split :: Integer -> [Integer]
split n = map read [take (div l 2) s, drop (div l 2) s]
  where
    s = show n
    l = length s

blink :: Integer -> [Integer]
blink n
  | n == 0 = [1]
  | even . length . show $ n = split n
  | otherwise = [n * 2024]

solve :: Integer -> Integer -> Integer
solve left n
  | left == 0 = 1
  | otherwise = sum . map (solve $ left - 1) $ blink n

main :: IO ()
main = do
  contents <- getContents
  let input = map read . words $ contents

  print $ sum . map (solve 25) $ input
