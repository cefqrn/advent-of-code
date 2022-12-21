from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

from typing import Optional

class Node:
    def __init__(self, value, prev=None, next=None):
        self.value: int = value
        self.prev: Optional[Node] = prev
        self.next: Optional[Node] = next

    def move(self):
        curr = self
        remaining = self.value

        if remaining > 0:
            self.next.prev = self.prev
            self.prev.next = self.next
            while remaining > 0:
                curr = curr.next
                remaining -= 1

            curr.next.prev = self
            self.prev = curr

            self.next = curr.next
            curr.next = self
        
        if remaining < 0:
            self.next.prev = self.prev
            self.prev.next = self.next
            while remaining < 0:
                curr = curr.prev
                remaining += 1

            curr.prev.next = self
            self.prev = curr.prev

            self.next = curr
            curr.prev = self
        

    def __iter__(self):
        yield self
        curr = self.next
        while curr is not self:
            yield curr
            curr = curr.next

    def skip(self, amount):
        curr = self
        for _ in range(amount):
            curr = curr.next

        return curr


prev = root = Node(ints[0])
nodes = [root]
for value in ints[1:]:
    curr = Node(value, prev)
    if value == 0:
        zero = curr
    nodes.append(curr)
    prev.next = curr
    prev = curr

curr.next = root
root.prev = curr

for i, node in enumerate(nodes):
    node.move()

    print([x.value for x in root])

s = zero.skip(1000).value
s += zero.skip(2000).value
s += zero.skip(3000).value

print(s)

# not -1245
