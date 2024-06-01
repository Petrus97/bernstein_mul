from enum import Enum, auto

# https://www.ti.com/sc/docs/products/micro/msp430/userguid/as_5.pdf
# Machine dependent costs
ADD_COST = 1
SUB_COST = 1
NEG_COST = 1
SHIFT_COST = 1
MULT_COST = 30 # same as cortex M0 small multiplier


class MulOp(Enum):
    """
    Enumeration of multiplication operations
    """

    IDENTITY = 0
    NEGATE = auto()
    SHIFT_ADD = auto()
    SHIFT_SUB = auto()
    SHIFT_REV = auto()
    FACTOR_ADD = auto()
    FACTOR_SUB = auto()
    FACTOR_REV = auto()


COSTS = {
    MulOp.IDENTITY: 0,  # Cost(1) = 0
    MulOp.NEGATE: NEG_COST,  # Cost(-1) = negateCost
    MulOp.SHIFT_ADD: SHIFT_COST + ADD_COST,
    MulOp.SHIFT_SUB: SHIFT_COST + SUB_COST,
    MulOp.SHIFT_REV: SHIFT_COST,
    MulOp.FACTOR_ADD: SHIFT_COST + ADD_COST,
    MulOp.FACTOR_SUB: SHIFT_COST + SUB_COST,
    MulOp.FACTOR_REV: SHIFT_COST + SUB_COST,
}
