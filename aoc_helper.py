from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import date
from pathlib import Path

from typing import Optional


DIRNAME = Path(__file__).parent

base_code = """import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *
"""


class CouldNotFetchError(Exception):
    def __init__(self, reason: Optional[str]=None):
        if reason is None:
            message = "Could not fetch input."
        else:
            message = f"Could not fetch input ({reason})."

        super().__init__(message)


class CookieError(Exception): ...


def get_cookie() -> str:
    try:
        with open(".cookie") as f:
            return f.read()
    except FileNotFoundError:
        raise CookieError(".cookie file missing")


def get_headers() -> dict[str, str]:
    return {
        "User-Agent": "cefqrn's pineapple script ( contact: cefqrn@gmail.com )",
        "Cookie": get_cookie()
    }


class Problem:
    def __init__(self, day: Optional[int]=None, year: Optional[int]=None):
        today = date.today()

        self.day = day if day is not None else today.day
        self.year = year if year is not None else today.year

        self._input: str | None = None
    
    @property
    def folder_path(self) -> Path:
        return DIRNAME / f"{self.year}" / f"{self.day:02}"
    
    @property
    def input_url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}/input"

    @property
    def input(self) -> str:
        if self._input is not None:
            return self._input

        try:
            headers = get_headers()
        except CookieError as e:
            raise CouldNotFetchError("Could not find cookie")
        
        try:
            with urlopen(Request(url=self.input_url, headers=headers)) as f:
                _input = f.read().decode("utf-8")
        except HTTPError as e:
            raise CouldNotFetchError(f"HTTP Error {e.code}")

        self._input = _input
        return _input

    def fetch_input(self) -> None:
        print(f"Fetching input for {self.year}-12-{self.day:02}...")

        try:
            day_input = self.input
        except CouldNotFetchError as e:
            print(e)
            return

        with open(self.folder_path / "input", "w") as f:
            f.write(day_input)

    def setup(self) -> None:
        print(f"Setting up files for {self.year}-12-{self.day:02}...")

        if self.folder_path.exists():
            choice = input("The folder for this day already exists.\nWould you like to overwrite it? (y/n)\n")
            if choice.lower() != "y":
                print("Setup cancelled.")
                return
                
            print("Overwriting...")
            if not self.folder_path.is_dir():
                self.folder_path.unlink()

        self.folder_path.mkdir(exist_ok=True)

        with open(self.folder_path / "initial.py", "w") as f:
            f.write(base_code)
        
        self.fetch_input()


def main(args: list[str]):
    if len(args) < 2:
        raise ValueError(f"usage: {args[0]} <command>")

    match(args[1]):
        case "s" | "setup":
            if len(args) < 2:
                raise ValueError(f"usage: {args[0]} setup | s, [ <day>, <year>? ]?")

            Problem(*map(int, args[2:])).setup()
            
        case "f" | "fetch":
            if len(args) < 2:
                raise ValueError(f"usage: {args[0]} fetch | f, [ <day>, <year>? ]?")

            Problem(*map(int, args[2:])).fetch_input()


if __name__ == "__main__":
    import sys
    main(sys.argv)
