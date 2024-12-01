import Data.List (sort)

count :: Eq a => a -> [a] -> Int
count c = length . filter (== c)

main :: IO ()
main = do
  contents <- getContents

  let parsedLines = map (map read . words) . lines $ contents

  let a = sort . map head $ parsedLines
  let b = sort . map last $ parsedLines

  print . sum . map abs $ zipWith (-) a b
  print . sum $ zipWith (*) a (map (flip count $ b) a)
