from collections import defaultdict

class DisjointSetUnion:
    def __init__(self, n):
        self.parents = list(range(n))
        self.rank = [0] * n

    def __getitem__(self, i):
        to_update = []
        while i != (parent := self.parents[i]):
            to_update.append(i)
            i = parent

        for j in to_update:
            self.parents[j] = i

        return i

    def union(self, i, j):
        i = self[i]
        j = self[j]
        if i == j:
            return False

        if self.rank[j] > self.rank[i]:
            i, j = j, i

        self.rank[i] += self.rank[i] == self.rank[j]
        self.parents[j] = i

        return True

    def to_sets(self):
        result = defaultdict(set)
        for i, rep in enumerate(self):
            result[rep].add(i)

        yield from result.values()
