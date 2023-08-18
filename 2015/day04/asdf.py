import hashlib
import multiprocessing
import itertools

chunk_size = 65536

def search_chunk(i):
    key, prefix, chunk_lower, chunk_upper = i

    for x in range(chunk_lower, chunk_upper):
        if hashlib.md5((key + str(x)).encode()).hexdigest().startswith(prefix):
            return x
    
    return None

def find_valid(key: str, prefix: str, limit: int):
    chunk_lowers = [i for i in range(0, limit, chunk_size)]
    chunk_uppers = [min(i + chunk_size, limit) for i in range(0, limit, chunk_size)]

    with multiprocessing.Pool() as pool:
        for n in pool.imap(search_chunk, zip(itertools.repeat(key), itertools.repeat(prefix), chunk_lowers, chunk_uppers)):
            if n is not None:
                return n
            
def part1(key):
    return find_valid(key, "0"*5, 10**7)

def part2(key):
    return find_valid(key, "0"*6, 10**7)

if __name__ == "__main__":
    from time import perf_counter
    st = perf_counter()
    print(part1("iwrupvqb"))
    print(perf_counter() - st)

    st = perf_counter()
    print(part2("iwrupvqb"))
    print(perf_counter() - st)


# import os
# from hashlib import md5
# from concurrent.futures import ProcessPoolExecutor

# def is_valid(data: str, prefix: str, chunk) -> int | None:
#     for i in chunk:
#         digest = md5(f"{data}{i}".encode()).hexdigest()
#         if digest.startswith(prefix):
#             return i

# def check_valid(data: str, prefix: str, limit: int) -> int | None:
#     n_workers = os.cpu_count()
#     with ProcessPoolExecutor(max_workers=n_workers) as executor:
#         futures = []
#         for thread in range(n_workers):
#             futures.append(
#                 executor.submit(
#                     is_valid, data, prefix,
#                     range(1 + thread, 10 ** limit + thread, n_workers)
#                 )
#             )
#         return min(t for f in futures if (t := f.result()))

# def part1(data: str):
#     return check_valid(data, "0"*5, 7)

# def part2(data: str):
#     return check_valid(data, "0"*6, 7)

# if __name__ == "__main__":
#     from time import perf_counter
#     st = perf_counter()
#     print(part1("iwrupvqb"))
#     print(perf_counter() - st)

#     st = perf_counter()
#     print(part2("iwrupvqb"))
#     print(perf_counter() - st)