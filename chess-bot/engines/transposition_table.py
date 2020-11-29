MAX_SIZE = 10000000  # 10 M

from collections import namedtuple

Node = namedtuple("Node", ["move", "value", "kind", "depth"])


def kind_to_int(kind):
    if kind == "exact":
        return 0
    if kind == "beta":
        return 1
    if kind == "alpha":
        return 2


def int_to_kind(_int):
    if _int == 0:
        return "exact"
    if _int == 1:
        return "beta"
    if _int == 2:
        return "alpha"


class TranspositionTable:
    def __init__(self):
        self.tt = {}

    def insert_node(self, zobriest_hash, move_uci, value, kind, depth):
        if len(self.tt) < MAX_SIZE:
            self.tt[zobriest_hash] = (
                zobriest_hash,
                move_uci,
                value,
                kind_to_int(kind),
                depth,
            )
        else:
            print("TranspositionTable full.")
            self.tt.clear()

    def get_node(self, zobriest_hash):
        node = self.tt.get(zobriest_hash)

        if node is not None and node[0] == zobriest_hash:
            return Node(node[1], node[2], int_to_kind(node[3]), node[4])

        return None