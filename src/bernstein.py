"""
R. Bernstein's algorithm for integer constant multiplication
"""

from hash_table import HashTable
from constants import MulOp, COSTS, NEG_COST, SHIFT_COST, MULT_COST
from node import Node
from utils import is_odd, make_odd

hash_table = HashTable()

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
    Factoring in the form 2^i ± 1.
    '''
    node = hash_table.lookup(c)
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

def multiply(target: int):
    multiply_cost = estimate_cost(target)
    if is_odd(target):  # 16a
        result: Node = find_sequence(target, multiply_cost)
        if (result.parent is not None) and (result.cost < multiply_cost):
            emit_code(result)
        else:
            print(f"Cost {result.cost} is higher than MUL instruction cost {multiply_cost}")
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
    parser.add_argument("-c", type=int, help="The constant to multiply. Default is 2.", default=2)
    args = parser.parse_args()
    constant = args.c
    print(constant)
    multiply(constant)

if __name__ == "__main__":
    main()
