import os
import sys
import datetime
import urllib.error
import urllib.request

from typing import Optional


DIRNAME = os.path.dirname(__file__)
HEADERS = {
    "User-Agent": "cefqrn's pineapple script ( contact: cefqrn@gmail.com )",
    "Cookie": f"{os.getenv('COOKIE')}"
}

base_code = """import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *
"""


class CouldNotFetchError(Exception):
    pass


def get_input(day: int, year: int) -> str:
    try:
        request = urllib.request.Request(
            f"https://adventofcode.com/{year}/day/{day}/input",
            headers=HEADERS
        )

        with urllib.request.urlopen(request) as f:
            return f.read().decode("utf-8")

    except urllib.error.HTTPError as e:
        raise CouldNotFetchError


def fetch(day: Optional[int]=None, year: Optional[int]=None) -> None:
    if day is None:
        day = datetime.date.today().day

    if year is None:
        year = datetime.date.today().year

    print(f"Fetching input for {year}-12-{day:02}...")

    day_folder_path = os.path.join(DIRNAME, f"{year}/{day:02}")

    try:
        day_input = get_input(day, year)
    except CouldNotFetchError:
        print("Could not fetch input.")
        return

    with open(os.path.join(day_folder_path, "input"), "w") as f:
        f.write(day_input)


def setup(day: Optional[int]=None, year: Optional[int]=None) -> None:
    if day is None:
        day = datetime.date.today().day

    if year is None:
        year = datetime.date.today().year
    
    print(f"Setting up files for {year}-12-{day:02}...")

    day_folder_path = os.path.join(DIRNAME, f"{year}/{day:02}")

    try:
        os.mkdir(day_folder_path)
    except FileExistsError:
        userInput = input("The folder already exists.\nWould you like to overwrite its files? (y/n)\n")
        if userInput.lower() != "y":
            print("Setup cancelled")
            return
            
        print("Overwriting files...")

    with open(os.path.join(day_folder_path, "initial.py"), "w") as f:
        f.write(base_code)
    
    fetch(day, year)


def main(args: list[str]):
    if len(args) < 2:
        raise ValueError(f"usage: {args[0]} <command>")

    match(args[1]):
        case "s" | "setup":
            if len(args) < 2:
                raise ValueError(f"usage: {args[0]} setup | s, [ <day>, <year>? ]?")

            setup(*map(int, args[2:]))
            
        case "f" | "fetch":
            if len(args) < 2:
                raise ValueError(f"usage: {args[0]} fetch | f, [ <day>, <year>? ]?")

            fetch(*map(int, args[2:]))


if __name__ == "__main__":
    main(sys.argv)
