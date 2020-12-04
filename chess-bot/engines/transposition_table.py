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


def compare_move_histories(requested, stored):
    # req = [move.uci() for move in requested]
    # sto = [move.uci() for move in stored]

    # different = False
    # for i in range(min(len(req), len(sto))):
    #     if req[i] != sto[i]:
    #         different = True
    #         break

    # if len(req) != len(sto):
    #     different = True

    if requested != stored:
        print(f"Move history requested: {requested}")
        print(f"Move history stored   : {stored}")
        print("-")


class TranspositionTable:
    def __init__(self):
        self._tt = {}

    def insert_node(
        self, zobriest_hash, move_uci, value, kind, depth
    ):  # , move_history=[]):
        if len(self._tt) < MAX_SIZE:
            # history = "|".join([move.uci() for move in move_history])
            self._tt[zobriest_hash] = (
                zobriest_hash,
                move_uci,
                value,
                kind_to_int(kind),
                depth,
                # history,
            )
        else:
            print("TranspositionTable full.")
            self._tt.clear()

    def get_node(self, zobriest_hash, stats):  # , _requested_move_history=[]):
        node = self._tt.get(zobriest_hash)

        if node is not None:
            if node[0] == zobriest_hash:
                # stored_move_history = node[5]
                # requested_move_history = "|".join(
                #     [move.uci() for move in _requested_move_history]
                # )
                # compare_move_histories(requested_move_history, stored_move_history)
                return Node(node[1], node[2], int_to_kind(node[3]), node[4])
            else:
                stats.inc_hash_collision()

        return None

    def __len__(self):
        return len(self._tt)