import math

s = 34000000


def sum_factors(n):
    s = 0
    for i in range(1, math.isqrt(n)+1):
        if n % i:
            continue

        s += i + n // i

    return s


def sum_valid_factors(n):
    n_fdiv_50 = n // 50
    s = 1 + n

    isqrt_n = math.isqrt(n)

    for i in range(2, isqrt_n + 1):
        if n % i:
            continue

        if i >= n_fdiv_50:
            s += i
        if (i2:=n//i) >= n_fdiv_50:
            s += i2
    
    if isqrt_n * isqrt_n == n:
        s -= isqrt_n

    return s


for i in range(s):
    if sum_factors(i)*10 >= s:
        print(f"p1: {i}")
        break

for i in range(1, s):
    if sum_valid_factors(i)*11 >= s:
        print(f"p2: {i}")
        break
