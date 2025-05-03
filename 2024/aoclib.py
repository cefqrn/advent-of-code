from itertools import islice, tee


def windowed(it, n):
    return list(zip(*[islice(x, i, None) for i, x in enumerate(tee(it, n))]))


def batched(it, n):
    return list(zip(*n*[iter(it)]))


def transposed(it):
    return list(zip(*it))


def rotated_cw(it, n=1):
    for _ in range(n % 4):
        it = list(map(reversed, transposed(it)))

    return it


def rotated_ccw(it, n=1):
    return rotated_cw(it, -n)
