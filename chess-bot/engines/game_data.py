import chess

from .zobrist_hash import ZobristHash


class GameData:
    def __init__(self, game_id):
        self._game_id = game_id
        self._color = None
        self._sign = None
        self._board = chess.Board()
        self._zobrist_hash = ZobristHash()
        self._zobrist_hash.from_board(self._board)
        self._move_history = []
        # self._hash_stack = [self._zobrist_hash.h()]

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board
        self._zobrist_hash.from_board(self._board)
        # self._hash_stack = [self._zobrist_hash.h()]

    @property
    def zobrist_hash(self):
        return self._zobrist_hash

    @property
    def game_id(self):
        return self._game_id

    @property
    def move_history(self):
        return self._move_history

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._sign = 1 if self._color == chess.WHITE else -1

    def opponent_color(self):
        return not self._color

    def push_move(self, move):
        # fen = self._board.fen()
        dropped_piece = self._board.piece_type_at(move.to_square)
        self._board.push(move)
        _hash = self._zobrist_hash.make_move(self._board, move, dropped_piece)
        # self._hash_stack.append(_hash)
        # _hash_fresh = ZobristHash().from_board(self._board)

        # if _hash != _hash_fresh:
        #     print("Hash problem:DO")
        #     print(f"Fen: {fen}")
        #     print(f"Uci: {move.uci()}")
        #     print(f"_hash: {_hash}")
        #     print(f"_hash_fresh: {_hash_fresh}")
        # else:
        #     print("No problem !")

        return _hash

    def pop_move(self):

        move = self._board.pop()  # move =
        _hash = self._zobrist_hash.undo_move(self._board, move)

        # _hash_from_stack = self._hash_stack[-2]
        # _hash_fresh = ZobristHash().from_board(self._board)

        # if _hash_from_stack != _hash_fresh or _hash != _hash_fresh:
        #     print("Hash problem:UNDO")
        #     print(f"Fen: {self._board.fen()}")
        #     print(f"Uci: {move.uci()}")
        #     print(f"stack: {self._hash_stack}")
        #     print(f"_hash_from_stack: {_hash_from_stack}")
        #     print(f"_hash: {_hash}")
        #     print(f"_hash_fresh: {_hash_fresh}")
        # else:
        #     print("No problem !")

        # self._hash_stack.pop()

        return _hash

    def get_sign(self):
        return self._sign
