"""
R. Bernstein's algorithm for integer constant multiplication
"""

from enum import Enum, auto
import numpy as np

# Machine dependent costs
ADD_COST = 1
SUB_COST = 1
NEG_COST = 1
SHIFT_COST = 1
MULT_COST = 8#  np.iinfo(np.int32).max


class MulOp(Enum):
    IDENTITY = 0
    NEGATE = auto()
    SHIFT_ADD = auto()
    SHIFT_SUB = auto()
    SHIFT_REV = auto()
    FACTOR_ADD = auto()
    FACTOR_SUB = auto()
    FACTOR_REV = auto()


COSTS = {
    MulOp.IDENTITY: 0,
    MulOp.NEGATE: NEG_COST,
    MulOp.SHIFT_ADD: SHIFT_COST + ADD_COST,
    MulOp.SHIFT_SUB: SHIFT_COST + SUB_COST,
    MulOp.SHIFT_REV: SHIFT_COST,
    MulOp.FACTOR_ADD: SHIFT_COST + ADD_COST,
    MulOp.FACTOR_SUB: SHIFT_COST + SUB_COST,
    MulOp.FACTOR_REV: SHIFT_COST + SUB_COST,
}


class Node:
    def __init__(
        self,
        parent=None,
        op: MulOp = MulOp.IDENTITY,
        value: int = 0,
        cost: int = 0,
        next=None,
    ):
        self.parent: Node = parent
        self.op: MulOp = op
        self.value: int = value
        self.cost: int = cost
        self.next: Node = None


class HashTable:
    def __init__(self):
        self.size = 31
        self.table: list[Node] = [None] * self.size

    def insert(self, node: Node):
        index = node.value % self.size
        if self.table[index] is None:
            self.table[index] = node
        else:
            node.next = self.table[index]
            self.table[index] = node

    def lookup(self, c: int):
        """
        Look for a node containing the given value in the hash table.
        If found, return the node. Otherwise, create a new node and return it.
        """
        index = abs(c) % self.size
        node = self.table[index]

        if node is not None:
            print(f"Collision detected c={c}")
            tmp = self.table[index]
            strstr = "\t"
            while tmp is not None:
                strstr += f" Node:{tmp.value} -> "
                tmp = tmp.next
            print(strstr)

        # check if the node is already in the hash table
        while (node is not None) and node.value != c:
            node = node.next
        # If the node is not found, create a new node
        if node is None:
            node = Node(
                parent=None, value=c, cost=SHIFT_COST
            )  # Create a new node
            node.next = self.table[index]
            self.table[index] = node  # Add the new node to the hash table
        return node

    def __lookup__(self, c: int):
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

    def print(self):
        for i in range(self.size):
            strstr = f"[{i}] -> "
            node = self.table[i]
            while node is not None:
                strstr += f"Node:{node.value} -> "
                node = node.next
            print(strstr)


# FIXME move to a separate file
hash_table = HashTable()


def init_multiply():
    node1 = hash_table.__lookup__(1)
    node1.parent = node1
    node1.op = MulOp.IDENTITY
    node1.cost = 0

    node = hash_table.__lookup__(-1)
    node.parent = node1
    node.op = MulOp.NEGATE
    node.cost = NEG_COST


def is_odd(n: int) -> bool:
    return n & 1


def is_even(n: int) -> bool:
    return not is_odd(n)


def estimate_cost(target: int) -> int:
    # FIXME: Implement a better cost estimation
    return MULT_COST


def emit_code(node: Node) -> int:
    source = -1
    target = node.value
    match node.op:
        case MulOp.IDENTITY:
            pass
        case MulOp.NEGATE:
            source = emit_code(node.parent)
            print(f"{target} = 0 - {source}; // NEGATE")
        case MulOp.SHIFT_ADD:
            source = emit_code(node.parent)
            emit_shift(target - 1, source)
            print(f"{target} = {target - 1} + 1; // SHIFT_ADD")
        case MulOp.SHIFT_SUB:
            source = emit_code(node.parent)
            emit_shift(target + 1, source)
            print(f"{target} = {target + 1} - 1; // SHIFT_SUB")
        case MulOp.SHIFT_REV:
            source = emit_code(node.parent)
            emit_shift(1 - target, source)
            print(f"{target} = 1 - {1 - target}; // SHIFT_REV")
        case MulOp.FACTOR_ADD:
            source = emit_code(node.parent)
            emit_shift(target - source, source)
            print(f"{target} = {target - source} + {source}; // FACTOR_ADD")
        case MulOp.FACTOR_SUB:
            source = emit_code(node.parent)
            emit_shift(target + source, source)
            print(f"{target} = {target + source} - {source}; // FACTOR_SUB")
        case MulOp.FACTOR_REV:
            source = emit_code(node.parent)
            emit_shift(source - target, source)
            print(f"{target} = {source} - {source-target}; // FACTOR_REV")
    return target


def emit_shift(target: int, source: int):
    temp = source
    i = 0
    while target != temp:
        temp <<= 1
        i += 1
    print(f"{target} = {source} << {i}; // SHIFT {i} times")


def do_try(factor: int, node: Node, op: MulOp):
    cost = COSTS[op]
    limit = node.cost - cost
    factor_node = find_sequence(factor, limit)
    if (factor_node.parent) and (factor_node.cost < limit):
        node.parent = factor_node
        node.op = op
        node.cost = factor_node.cost + cost


def find_sequence(c: int, limit: int) -> Node:
    '''
    Factoring in the form 2^i +- 1. i = 4
    '''
    node = hash_table.__lookup__(c)
    if (node.parent is None) and (node.cost < limit):
        node.cost = limit
        if c > 0: 
            # 9a positive case
            power = 4
            edge = c >> 1
            while power < edge:
                if c % (power - 1) == 0:
                    do_try(int(c / (power - 1)), node, MulOp.FACTOR_SUB)
                if c % (power + 1) == 0:
                    do_try(int(c / (power + 1)), node, MulOp.FACTOR_ADD)
                power <<= 1
            do_try(make_odd(c - 1), node, MulOp.SHIFT_ADD)
            do_try(make_odd(c + 1), node, MulOp.SHIFT_SUB)
        else:  
            # 9b negative case
            power = 4
            edge = (-c) >> 1
            while power < edge:
                if c % (1 - power) == 0:
                    do_try(c / (1 - power), node, MulOp.FACTOR_REV)
                if c % (power + 1) == 0:
                    do_try(c / (power + 1), node, MulOp.FACTOR_ADD)
                power <<= 1
            do_try(make_odd(1 - c), node, MulOp.SHIFT_REV)
            do_try(make_odd(c + 1), node, MulOp.SHIFT_SUB)
    return node


def make_odd(n: int) -> int:
    while True:
        n >>= 1
        if is_odd(n):
            return n


def multiply(target: int):
    multiply_cost = estimate_cost(target)
    if is_odd(target):  # 16a
        result: Node = find_sequence(target, multiply_cost)
        if (result.parent is not None) and (result.cost < multiply_cost):
            emit_code(result)
        else:
            print("use multiply instruction")
    else:  # 16b
        result: Node = find_sequence(make_odd(target), multiply_cost - SHIFT_COST)
        if (result.parent is not None) and (result.cost + SHIFT_COST < multiply_cost):
            source = emit_code(result)
            emit_shift(target, source)


def main():
    import argparse as ap

    parser = ap.ArgumentParser(
        description="R. Bernstein's algorithm for integer constant multiplication"
    )
    parser.add_argument("-c", type=int, help="The constant to multiply", default=2)
    args = parser.parse_args()
    constant = args.c
    print(constant)
    init_multiply()
    multiply(constant)
    # hash_table.print()


if __name__ == "__main__":
    main()
