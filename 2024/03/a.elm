{- thanks to
   http://cmsc-16100.cs.uchicago.edu/2021-autumn/Lectures/18/functional-parsing.php
   and
   http://cmsc-16100.cs.uchicago.edu/2021-autumn/Lectures/18/documents/parsers.pdf
-}

import Browser
import Html exposing (Html, div, input, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)

type Msg =
  Change String

type alias Model =
  String

type Operation
  = Mul Int Int
  | Do
  | Dont
  | Nop

type alias Stream =
  { data: List Char
  , buffer: List Char
  }

type alias Parser a =
  List Char -> Maybe (a, List Char)

satisfy : (Char -> Bool) -> Parser Char
satisfy p s =
  case s of
    [] -> Nothing
    (x::xs) ->
      if p x then Just (x, xs)
      else Nothing

char : Char -> Parser Char
char c = satisfy (\x -> x == c)

string : String -> Parser String
string x s =
  case s of
    [] -> Nothing
    _ ->
      if (String.fromList <| List.take (String.length x) s) == x then Just
        (x, List.drop (String.length x) s)
      else Nothing

combine : Parser a -> Parser b -> Parser (a, b)
combine x y s =
  case x s of
    Nothing -> Nothing
    Just (v1, s1) ->
      case y s1 of
        Nothing -> Nothing
        Just (v2, s2) ->
          Just ((v1, v2), s2)

tryElse : Parser a -> Parser a -> Parser a
tryElse x y s =
  case x s of
    Nothing -> y s
    Just r -> Just r

takeWhile: (a -> Bool) -> List a -> List a
takeWhile f l =
  case l of
    [] -> []
    (x::xs) ->
      if f x then
        x :: takeWhile f l
      else
        takeWhile f l

digit : Parser Int
digit s =
  case satisfy Char.isDigit s of
    Nothing -> Nothing
    Just (v, r) -> Just ((Char.toCode v) - 48, r)

number : Parser Int
number s =
  case digit s of
    Nothing -> Nothing
    Just (v1, r1) ->
      case number r1 of
        Nothing -> Just (v1, r1)
        Just (v2, r2) -> Just ((10 ^ (List.length r1 - List.length r2)) * v1 + v2, r2)

apply : Parser a -> (a -> b) -> Parser b
apply x f s =
  case x s of
    Nothing -> Nothing
    Just (v, r) -> Just (f v, r)

ignore : Parser Operation
ignore = apply (satisfy (\_ -> True)) (\_ -> Nop)

parseMul : Parser Operation
parseMul =
  apply
    (  combine (string "mul(")
    <| combine number
    <| combine (char ',')
    <| combine number(char ')')
    )
    (\(_, (a, (_, (b, _)))) -> Mul a b)

parseDo : Parser Operation
parseDo =
  apply (string "do()") (\_ -> Do)

parseDont : Parser Operation
parseDont =
  apply (string "don't()") (\_ -> Dont)

parseP1 : List Char -> List Operation
parseP1 s =
  case (
       tryElse parseMul ignore
  ) s of
    Nothing -> []
    Just (Nop, r) -> parseP1 r
    Just (v, r) -> v :: parseP1 r

parseP2 : List Char -> List Operation
parseP2 s =
  case (
       tryElse parseMul
    <| tryElse parseDo
    <| tryElse parseDont ignore
  ) s of
    Nothing -> []
    Just (Nop, r) -> parseP2 r
    Just (v, r) -> v :: parseP2 r

evaluate : Bool -> List Operation -> Int
evaluate enabled operations =
  case operations of
    [] -> 0
    (x::xs) ->
      case x of
        Mul a b ->
          (if enabled then a*b else 0) + evaluate enabled xs

        Do ->
          evaluate True xs

        Dont ->
          evaluate False xs

        Nop ->
          evaluate enabled xs

main =
  Browser.sandbox
    { init = init
    , update = update
    , view = view
    }

init : Model
init = ""

update : Msg -> Model -> Model
update msg model =
  case msg of
    Change s -> s

view : Model -> Html Msg
view model =
  let
    p1 = String.fromInt <| evaluate True <| parseP1 (String.toList model)
    p2 = String.fromInt <| evaluate True <| parseP2 (String.toList model)
  in
    div []
      [ input [ placeholder "enter puzzle input here", value model, onInput Change ] []
      , div [] [text p1]
      , div [] [text p2]
      ]
