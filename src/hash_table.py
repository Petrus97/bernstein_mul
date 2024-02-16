from node import Node
from constants import SHIFT_COST, NEG_COST, MulOp


class HashTable:
    def __init__(self, size: int = 31):
        self.size = size
        self.table: list[Node] = [None] * self.size
        self.__init_table__()

    def lookup(self, c: int):
        """
        Lookup a node in the hash table.
        If the node is not found, create a new node and return it.
        """
        index = abs(c) % self.size
        node = self.table[index]
        if node is None:
            node = Node(parent=None, value=c, cost=SHIFT_COST)
            self.table[index] = node
            node.next = None
            return node
        else:
            while (node is not None) and (node.value != c):
                node = node.next
            if node is None:
                node = Node(parent=None, value=c, cost=SHIFT_COST)
                node.next = self.table[index]
                self.table[index] = node
                return node
            else:
                return node

    def print_table(self):
        for i in range(self.size):
            strstr = f"[{i}] -> "
            node = self.table[i]
            while node is not None:
                strstr += f"Node:{node.value} -> "
                node = node.next
            print(strstr)

    def __init_table__(self):
        """
        Initialize the hash table with the nodes for 1 and -1
        """
        node1 = self.lookup(1)
        node1.parent = node1
        node1.op = MulOp.IDENTITY
        node1.cost = 0

        node = self.lookup(-1)
        node.parent = node1
        node.op = MulOp.NEGATE
        node.cost = NEG_COST
