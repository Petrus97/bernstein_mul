from constants import MulOp


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
        self.next: Node = next
