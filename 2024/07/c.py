def concat(a, b):
    return int(str(a) + str(b))

p1 = p2 = 0
def solve(needed, nums, concat_used=False):
    global p1, p2

    if len(nums) < 2:
        if nums[0] != needed:
            return False

        p2 += needed
        if not concat_used:
            p1 += needed

        return True

    a, b = nums[:2]

    nums[1] = a + b
    if solve(needed, nums[1:], concat_used):
        return True

    nums[1] = a * b
    if solve(needed, nums[1:], concat_used):
        return True

    nums[1] = concat(a, b)
    if solve(needed, nums[1:], True):
        return True

    return False

with open(0) as f:
    for line in f:
        needed_str, nums_str = line.split(": ")
        solve(int(needed_str), list(map(int, nums_str.split())))

print(p1, p2)
