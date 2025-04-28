# data class for node of int and next node:
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    value: int
    next: Optional['Node'] = None

print('definition start')
node3 = Node(value=3, next=None)
node2 = Node(2, node3)
node1 = Node(1, node2)
print('end')

print('printer start')
cur = node1
while cur.next:
    print(cur.value)
    cur = cur.next
print(cur.value)
print('printer end')
