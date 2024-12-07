concat' :: Integer -> Integer -> Integer
concat' a b = read $ show a ++ show b

solve :: Bool -> Integer -> [Integer] -> (Integer, Integer)
solve _ _ [] = error "impossible"
solve concatUsed needed (have:[])
  | have /= needed = (0, 0)
  | concatUsed = (0,      needed)
  | otherwise  = (needed, needed)
solve concatUsed needed (a:b:xs)
  | let (p1, p2) = solve concatUsed needed (a+b:xs), 0 < p2 = (p1, p2)
  | let (p1, p2) = solve concatUsed needed (a*b:xs), 0 < p2 = (p1, p2)
  | let (p1, p2) = solve True needed (concat' a b:xs), 0 < p2 = (p1, p2)
  | otherwise = (0, 0)

parseLine :: String -> (Integer, [Integer])
parseLine s = (needed, nums)
  where
    needed = read . init . head . words $ s
    nums = map read . tail . words $ s

main :: IO ()
main = do
  contents <- getContents

  let results = map (uncurry $ solve False) . map parseLine . lines $ contents
  putStrLn $ (show . sum . map fst) results ++ " " ++ (show . sum . map snd) results
