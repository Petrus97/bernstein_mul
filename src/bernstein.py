"""
R. Bernstein's algorithm for integer constant multiplication
"""

from hash_table import HashTable
from constants import MulOp, COSTS, NEG_COST, SHIFT_COST, MULT_COST
from node import Node
from utils import is_odd, make_odd
from code_gen import CodeGen, Lang

hash_table = HashTable()
code_gen = None


def estimate_cost(target: int) -> int:
    # FIXME: Implement a better cost estimation
    return MULT_COST


num_op = 0


def emit_code(node: Node, code_gen: CodeGen) -> int:
    global num_op
    source = -1
    target = node.value
    match node.op:
        case MulOp.IDENTITY:
            pass
        case MulOp.NEGATE:
            source = emit_code(node.parent, code_gen=code_gen)
            print(f"{target} = 0 - {source}; // NEGATE")
            code_gen.gen_negate(target, source)
        case MulOp.SHIFT_ADD:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(target - 1, source, code_gen=code_gen)
            print(f"{target} = {target - 1} + 1; // SHIFT_ADD")
            code_gen.gen_add(target, target - 1, 1)
        case MulOp.SHIFT_SUB:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(target + 1, source, code_gen=code_gen)
            print(f"{target} = {target + 1} - 1; // SHIFT_SUB")
            code_gen.gen_sub(target, target + 1, 1)
        case MulOp.SHIFT_REV:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(1 - target, source, code_gen=code_gen)
            print(f"{target} = 1 - {1 - target}; // SHIFT_REV")
            code_gen.gen_sub(target, 1, 1 - target)
        case MulOp.FACTOR_ADD:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(target - source, source, code_gen=code_gen)
            print(f"{target} = {target - source} + {source}; // FACTOR_ADD")
            code_gen.gen_add(target, target - source, source)
        case MulOp.FACTOR_SUB:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(target + source, source, code_gen=code_gen)
            print(f"{target} = {target + source} - {source}; // FACTOR_SUB")
            code_gen.gen_sub(target, target + source, source)
        case MulOp.FACTOR_REV:
            source = emit_code(node.parent, code_gen=code_gen)
            emit_shift(source - target, source, code_gen=code_gen)
            print(f"{target} = {source} - {source-target}; // FACTOR_REV")
            code_gen.gen_sub(target, source, source - target)
    if node.op != MulOp.IDENTITY:
        num_op += 1
    return target


def emit_shift(target: int, source: int, code_gen: CodeGen):
    global num_op
    temp = source
    i = 0
    while target != temp:
        temp <<= 1
        i += 1
    print(f"{target} = {source} << {i}; // SHIFT {i} times")
    code_gen.gen_shift(target, source, i)
    num_op += 1


def do_try(factor: int, node: Node, op: MulOp):
    cost = COSTS[op]
    limit = node.cost - cost
    factor_node = find_sequence(factor, limit)
    if (factor_node.parent) and (factor_node.cost < limit):
        node.parent = factor_node
        node.op = op
        node.cost = factor_node.cost + cost


def find_sequence(c: int, limit: int) -> Node:
    """
    Factoring in the form 2^i ± 1.
    """
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
                    do_try(int(c / (1 - power)), node, MulOp.FACTOR_REV)
                if c % (power + 1) == 0:
                    do_try(int(c / (power + 1)), node, MulOp.FACTOR_ADD)
                power <<= 1
            do_try(make_odd(1 - c), node, MulOp.SHIFT_REV)
            do_try(make_odd(c + 1), node, MulOp.SHIFT_SUB)
    return node


def multiply(target: int, code_gen: CodeGen):
    multiply_cost = estimate_cost(target)
    if is_odd(target):  # 16a
        result: Node = find_sequence(target, multiply_cost)
        if (result.parent is not None) and (result.cost < multiply_cost):
            emit_code(result, code_gen)
        else:
            print(
                f"Cost {result.cost} is higher than MUL instruction cost {multiply_cost}"
            )
    else:  # 16b
        result: Node = find_sequence(make_odd(target), multiply_cost - SHIFT_COST)
        if (result.parent is not None) and (result.cost + SHIFT_COST < multiply_cost):
            source = emit_code(result, code_gen)
            emit_shift(target, source, code_gen)


def main():
    import argparse as ap

    parser = ap.ArgumentParser(
        description="R. Bernstein's algorithm for integer constant multiplication"
    )
    parser.add_argument(
        "-c", type=int, help="The constant to multiply. Default is 2.", default=2
    )
    args = parser.parse_args()
    constant = args.c
    # code_gen = CodeGen(target=constant, lang=Lang.C)
    # multiply(constant, code_gen)
    # print("Number of operations:", num_op)
    # code_gen.gen_code()
    # #######
    
    int8_numbers = range(-128, 128)
    if(constant == 0 or constant == 1):
        return
    # print(constant)
    for i in int8_numbers:
        if i == 0 or i == 1:
            continue
        code_gen = CodeGen(target=i, lang=Lang.C)
        multiply(i, code_gen)
        # print("Number of operations:", num_op)
        # num_op = 0
        code_gen.gen_code()
        code_gen.reset()
    with open("generated/c/multiply.h", "a") as f:
        f.write("\n")
        f.write(f"#endif\n")
        f.write("\n")
    # print(code_gen.temporaries_list)
    


if __name__ == "__main__":
    main()
