import chess

from .zobrist_hash import ZobristHash


class GameData:
    def __init__(self, game_id):
        self._game_id = game_id
        self._color = None
        self._board = chess.Board()
        self._zobrist_hash = ZobristHash()
        self._zobrist_hash.from_board(self._board)
        self._move_history = []

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board
        self._zobrist_hash.from_board(self._board)

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

    def opponent_color(self):
        return not self._color

    def push_move(self, move):
        self._board.push(move)
        # self._zobrist_hash.make_move(self._board, move)
        return self._zobrist_hash.from_board(self._board)
        # return self._zobrist_hash.h()

    def pop_move(self):
        self._board.pop()  # move =
        # self._zobrist_hash.undo_move(self._board, move)
        return self._zobrist_hash.from_board(self._board)
        # return self._zobrist_hash.h()


# fen = "r1bqkb1r/pppppppp/2n5/4P3/3P4/2N2N1P/PPP2nP1/R1BQKB1R w KQq - 0 7"

# game_data_ = GameData(1)
# game_data_.board = chess.Board(fen)

# print("\n\ninitial pos:")
# print(game_data_.zobrist_hash.h())
# move = chess.Move.from_uci("a2a3")
# print(move.from_square)
# print(move.to_square)
# game_data_.push_move(move)
# print("move done:")
# print(game_data_.zobrist_hash.h())
# game_data_.pop_move()
# print("move undone:")
# print(game_data_.zobrist_hash.h())

# print("\n\ninitial pos:")
# print(game_data_.zobrist_hash.h())
# move = chess.Move.from_uci("e1f2")
# print(move.from_square)
# print(move.to_square)
# game_data_.push_move(move)
# print("move done:")
# print(game_data_.zobrist_hash.h())
# game_data_.pop_move()
# print("move undone:")
# print(game_data_.zobrist_hash.h())

# fen2 = "rnb2bnr/pppPkppp/4p3/2q5/3P4/8/PPP2PPP/RNBQKBNR w KQ - 1 6"

# game_data_.board = chess.Board(fen2)
# print("\n\ninitial pos:")
# print(game_data_.zobrist_hash.h())

# move = chess.Move.from_uci("d7d8q")
# print(move.promotion)
# print(move.from_square)
# print(move.to_square)

# game_data_.push_move(move)
# print(game_data_.board.fen())
# print("move done:")
# print(game_data_.zobrist_hash.h())

# h = ZobristHash()
# h.from_board(game_data_.board)
# print(h.h())

# game_data_.pop_move()
# print("move undone:")
# print(game_data_.zobrist_hash.h())


# game_data_.board = chess.Board(
#     "rnbQ1bnr/ppp1kppp/4p3/2q5/3P4/8/PPP2PPP/RNBQKBNR b KQ - 0 6"
# )
# print("\n\ninitial pos:")
# print(game_data_.zobrist_hash.h())
