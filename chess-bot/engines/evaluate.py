import chess

from .random_fens import random_fens
from .game_data import GameData
from .piece_square_table import PIECE_POS_VALUES_MG, PIECE_VALUES
from .pieces import PIECES

PAWN_O = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

KNIGHT_O = [
    [-50, -40, -30, -30, -30, -30, -40, -50,],
    [-40, -20, 0, 0, 0, 0, -20, -40,],
    [-30, 0, 10, 15, 15, 10, 0, -30,],
    [-30, 5, 15, 20, 20, 15, 5, -30,],
    [-30, 0, 15, 20, 20, 15, 0, -30,],
    [-30, 5, 10, 15, 15, 10, 5, -30,],
    [-40, -20, 0, 5, 5, 0, -20, -40,],
    [-50, -40, -30, -30, -30, -30, -40, -50,],
]

BISHOP_O = [
    [-20, -10, -10, -10, -10, -10, -10, -20,],
    [-10, 0, 0, 0, 0, 0, 0, -10,],
    [-10, 0, 5, 10, 10, 5, 0, -10,],
    [-10, 5, 5, 10, 10, 5, 5, -10,],
    [-10, 0, 10, 10, 10, 10, 0, -10,],
    [-10, 10, 10, 10, 10, 10, 10, -10,],
    [-10, 5, 0, 0, 0, 0, 5, -10,],
    [-20, -10, -10, -10, -10, -10, -10, -20,],
]

ROOK_O = [
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [5, 10, 10, 10, 10, 10, 10, 5,],
    [-5, 0, 0, 0, 0, 0, 0, -5,],
    [-5, 0, 0, 0, 0, 0, 0, -5,],
    [-5, 0, 0, 0, 0, 0, 0, -5,],
    [-5, 0, 0, 0, 0, 0, 0, -5,],
    [-5, 0, 0, 0, 0, 0, 0, -5,],
    [0, 0, 0, 5, 5, 0, 0, 0,],
]

QUEEN_O = [
    [-20, -10, -10, -5, -5, -10, -10, -20,],
    [-10, 0, 0, 0, 0, 0, 0, -10,],
    [-10, 0, 5, 5, 5, 5, 0, -10,],
    [-5, 0, 5, 5, 5, 5, 0, -5,],
    [0, 0, 5, 5, 5, 5, 0, -5,],
    [-10, 5, 5, 5, 5, 5, 0, -10,],
    [-10, 0, 5, 0, 0, 0, 0, -10,],
    [-20, -10, -10, -5, -5, -10, -10, -20,],
]

KING_O = [
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0,],
]


PAWN = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    10,
    10,
    20,
    30,
    30,
    20,
    10,
    10,
    5,
    5,
    10,
    25,
    25,
    10,
    5,
    5,
    0,
    0,
    0,
    20,
    20,
    0,
    0,
    0,
    5,
    -5,
    -10,
    0,
    0,
    -10,
    -5,
    5,
    5,
    10,
    10,
    -20,
    -20,
    10,
    10,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

KNIGHT = [
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
    -40,
    -20,
    0,
    0,
    0,
    0,
    -20,
    -40,
    -30,
    0,
    10,
    15,
    15,
    10,
    0,
    -30,
    -30,
    5,
    15,
    20,
    20,
    15,
    5,
    -30,
    -30,
    0,
    15,
    20,
    20,
    15,
    0,
    -30,
    -30,
    5,
    10,
    15,
    15,
    10,
    5,
    -30,
    -40,
    -20,
    0,
    5,
    5,
    0,
    -20,
    -40,
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
]

BISHOP = [
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    10,
    10,
    5,
    0,
    -10,
    -10,
    5,
    5,
    10,
    10,
    5,
    5,
    -10,
    -10,
    0,
    10,
    10,
    10,
    10,
    0,
    -10,
    -10,
    10,
    10,
    10,
    10,
    10,
    10,
    -10,
    -10,
    5,
    0,
    0,
    0,
    0,
    5,
    -10,
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
]

ROOK = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    10,
    10,
    10,
    10,
    10,
    10,
    5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    0,
    0,
    0,
    5,
    5,
    0,
    0,
    0,
]

QUEEN = [
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -5,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    -10,
    5,
    5,
    5,
    5,
    5,
    0,
    -10,
    -10,
    0,
    5,
    0,
    0,
    0,
    0,
    -10,
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
]

ROOK = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

KING = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

# PIECE_POS_VALUES = {
#     chess.PAWN: PAWN,
#     chess.KNIGHT: KNIGHT,
#     chess.BISHOP: BISHOP,
#     chess.ROOK: ROOK,
#     chess.QUEEN: QUEEN,
#     chess.KING: KING,
# }

# PIECE_VALUES = {
#     chess.PAWN: 100,
#     chess.KNIGHT: 300,
#     chess.BISHOP: 300,
#     chess.ROOK: 500,
#     chess.QUEEN: 900,
#     chess.KING: 9000,
# }


def get_piece_value(piece, square, is_white):
    square = square if is_white else chess.square_mirror(square)

    y = chess.square_rank(square)
    x = chess.square_file(square)

    piece_val = PIECE_VALUES[piece.piece_type]
    pos = (y * 8) + x
    piece_pos_val = PIECE_POS_VALUES_MG[piece.piece_type][pos]

    sign = 1 if is_white else -1
    return sign * (piece_val + piece_pos_val)


def evaluate_position_o(game_data):
    board = game_data.board

    if board.is_checkmate():
        return -10000 if board.turn == chess.WHITE else +10000
    if board.is_stalemate():
        return 0

    total = 0

    for x in range(8):
        for y in range(8):
            square = chess.square(x, y)
            # print(f"square: {chess.square_name(square)}")

            piece = board.piece_at(square)
            # print(f"piece: {piece}")

            if piece is not None:
                is_white = piece.color == chess.WHITE
                total += get_piece_value(piece, square, is_white)

    return total

def evaluate_position(game_data):
    board = game_data.board

    if board.is_checkmate():
        print("Checkmate detected")
        return -9000 if board.turn == chess.WHITE else +9000
    if board.is_stalemate():
        return 0

    total = 0
    for piece in PIECES:
        # print(piece)

        pieces_white = board.pieces(piece, chess.WHITE)
        pieces_black = board.pieces(piece, chess.BLACK)

        count_white = len(pieces_white)
        count_black = len(pieces_black)
        material = (count_white - count_black) * PIECE_VALUES[piece]

        table = PIECE_POS_VALUES_MG[piece]
        pos_white = sum([table[i] for i in pieces_white])
        pos_black = sum([table[chess.square_mirror(i)] for i in pieces_black])
        positional = pos_white - pos_black

        # print(f"pos_white {pos_white}")
        # print(f"pos_black {pos_black}")
        # print(f"material {material}")
        # print(f"positional {positional}")
        total += material + positional

    # print(f"total: {total}")
    return total


# fen = "r1bqkb1r/pppppppp/2n5/4P3/3P4/2N2N1P/PPP2nP1/R1BQKB1R w KQq - 0 7"
# fen2 = "r1bqkb1r/pppppppp/2n4n/4P3/3P4/2N2N1P/PPP2PP1/R1BQKB1R w KQq - 1 7"  # better


# def print_score_of_fen(fen):
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.WHITE
#     score = evaluate_position(game_data)
#     print(f"score: {score}")


# print_score_of_fen(fen)
# print_score_of_fen(fen2)

# import time

# start_time = time.time()
# i = 1
# for fen in random_fens:
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.WHITE
#     old = evaluate_position_o(game_data)
#     print(f"- {i} -----------------------")
#     print(f"new: {new}")
#     print(f"old: {old}")
#     i += 1
# print("OLD --- %s seconds ---" % (time.time() - start_time))


# start_time = time.time()
# i = 1
# for fen in random_fens:
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.WHITE
#     new = evaluate_position(game_data)
#     print(f"- {i} -----------------------")
#     print(f"new: {new}")
#     print(f"old: {old}")
#     i += 1
# print("NEW --- %s seconds ---" % (time.time() - start_time))


# i = 1
# for fen in random_fens:
#     game_data = GameData(1)
#     game_data.board = chess.Board(fen)
#     game_data.color = chess.WHITE
#     new = evaluate_position(game_data)
#     old = evaluate_position_o(game_data)
#     print(f"- {i} -----------------------")
#     print(f"new: {new}")
#     print(f"old: {old}")
#     i += 1
