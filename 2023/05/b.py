from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]


def lowest_location(seed_ranges):
    lowest = float("inf")
    while seed_ranges:
        range_conversions, lo, hi = seed_ranges.pop()
        try:
            conversion, *remaining_conversions = range_conversions
        except ValueError:
            lowest = min(lowest, lo)
            continue

        for dest, source_lowest, length in conversion:
            source_highest = source_lowest+length-1
            if lo <= source_highest and source_lowest < hi:
                seed_ranges.append((
                    remaining_conversions,
                    range(dest, dest+length)[range(source_lowest, source_lowest+length).index(max(lo, source_lowest))],
                    range(dest, dest+length)[range(source_lowest, source_lowest+length).index(min(hi, source_highest))]
                ))

                if lo < source_lowest:
                    seed_ranges.append((remaining_conversions, lo, source_lowest))

                lo = source_lowest+length
                if lo >= hi:
                    break
        else:
            seed_ranges.append((remaining_conversions, lo, hi))

    return lowest


blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]

seeds, *blocks = blocks
seeds = tuple(map(int, seeds[0].split()[1:]))

conversions = [sorted((tuple(map(int, y.split())) for y in x[1:]), key=lambda x: x[1]) for x in blocks]

print(
    lowest_location([(conversions, seed, seed+1) for seed in seeds]),
    lowest_location([(conversions, lo, lo+range_length) for lo, range_length in zip(*2*[iter(seeds)])])
)
