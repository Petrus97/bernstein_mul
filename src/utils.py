
def is_odd(n: int) -> bool:
    return n & 1


def is_even(n: int) -> bool:
    return not is_odd(n)

def make_odd(n: int) -> int:
    while True:
        n >>= 1
        if is_odd(n):
            return n